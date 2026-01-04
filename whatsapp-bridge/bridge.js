
import makeWASocket, {
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion,
    makeCacheableSignalKeyStore
} from '@whiskeysockets/baileys';
import { Boom } from '@hapi/boom';
import qrcodeTerminal from 'qrcode-terminal';
import QRCode from 'qrcode';
import pino from 'pino';
import express from 'express';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let lastQR = null;
let isConnected = false;
let sock = null;

// Initialize Express immediately
const app = express();
app.use(bodyParser.json());

app.get('/qr', async (req, res) => {
    console.log(`🔍 [GET /qr] isConnected: ${isConnected}, lastQR: ${lastQR ? 'present' : 'null'}`);
    if (isConnected) {
        return res.send('<h1>✅ WhatsApp ya está conectado!</h1>');
    }
    if (!lastQR) {
        return res.send('<h1>⏳ Esperando a que se genere el código QR... Refresca en unos segundos.</h1>');
    }

    try {
        const qrImageUrl = await QRCode.toDataURL(lastQR);
        res.send(`
            <html>
                <body style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; background-color: #f0f2f5;">
                    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;">
                        <h2 style="color: #128c7e;">Escanea el código QR</h2>
                        <p>Abre WhatsApp en tu teléfono > Menú > Dispositivos vinculados</p>
                        <img src="${qrImageUrl}" style="width: 300px; height: 300px; margin: 20px 0;" />
                        <p style="color: #666; font-size: 0.9em;">El QR se actualiza automáticamente si expira.</p>
                    </div>
                    <script>
                        setInterval(async () => {
                            try {
                                const resp = await fetch('/status');
                                const data = await resp.json();
                                if (data.connected) location.reload();
                            } catch (e) {}
                        }, 5000);
                    </script>
                </body>
            </html>
        `);
    } catch (err) {
        res.status(500).send('Error generando QR');
    }
});

app.get('/status', (req, res) => {
    res.json({ connected: isConnected });
});

app.post('/send', async (req, res) => {
    const { number, text } = req.body;

    if (!number || !text) {
        return res.status(400).json({ error: 'Faltan parámetros: number o text' });
    }

    if (!isConnected || !sock) {
        return res.status(503).json({ error: 'WhatsApp no está conectado' });
    }

    try {
        let jid = number;
        if (!jid.includes('@')) {
            // Si solo es el número, limpiar y añadir el sufijo estándar
            jid = jid.replace(/\D/g, '') + '@s.whatsapp.net';
        }

        console.log(`🚀 Enviando mensaje a ${jid}...`);
        await sock.sendMessage(jid, { text });

        res.json({ success: true, message: 'Enviado correctamente' });
    } catch (error) {
        console.error('❌ Error enviando mensaje:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

const PORT = 3001;
const HOST = '0.0.0.0';
app.listen(PORT, HOST, () => {
    console.log(`🌐 Bridge API escuchando en http://${HOST}:${PORT}`);
    console.log(`🔗 Ver QR en: http://localhost:${PORT}/qr`);
});

async function startBridge() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
    const { version, isLatest } = await fetchLatestBaileysVersion();

    console.log(`📡 Usando Baileys v${version.join('.')}, isLatest: ${isLatest}`);

    sock = makeWASocket({
        version,
        logger: pino({ level: 'error' }),
        printQRInTerminal: false, // Ya no es necesario con la web
        auth: {
            creds: state.creds,
            keys: makeCacheableSignalKeyStore(state.keys, pino({ level: 'error' })),
        },
        generateHighQualityLinkPreview: true,
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            lastQR = qr;
            console.log('📸 Nuevo código QR generado. Escanéalo en http://localhost:3000/qr');
            qrcodeTerminal.generate(qr, { small: true });
        }

        if (connection === 'close') {
            isConnected = false;
            const statusCode = (lastDisconnect.error instanceof Boom) ?
                lastDisconnect.error.output?.statusCode : 0;

            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            console.log(`❌ Conexión cerrada (${statusCode}). Reconectando: ${shouldReconnect}`);

            if (shouldReconnect) {
                setTimeout(startBridge, 5000); // Wait 5s before reconnecting
            }
        } else if (connection === 'open') {
            isConnected = true;
            lastQR = null;
            console.log('✅ Conexión establecida con éxito!');
        }
    });

    sock.ev.on('messages.upsert', async (m) => {
        if (m.type !== 'notify') return;

        for (const msg of m.messages) {
            if (!msg.message || msg.key.fromMe) continue;

            const sender = msg.key.remoteJid;
            const text = msg.message.conversation ||
                msg.message.extendedTextMessage?.text ||
                msg.message.buttonsResponseMessage?.selectedButtonId || '';

            if (!text) continue;

            console.log(`📩 Nuevo mensaje de ${sender}: ${text}`);
            console.dir(msg, { depth: null });

            // Trigger Python processing
            const pythonScript = path.join(__dirname, '../src/messaging/process_incoming.py');
            const pythonProcess = spawn('python3', [pythonScript, sender, text]);

            pythonProcess.stdout.on('data', (data) => {
                console.log(`🐍 [Python STDOUT]: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`🐍 [Python STDERR]: ${data}`);
            });
        }
    });
}

startBridge().catch(err => console.error('Error fatal:', err));
