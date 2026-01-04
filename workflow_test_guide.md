## 1. Datos del Negocio de Prueba
He creado un archivo llamado `data/test_business.csv` con un negocio ficticio: **Reformas Maverick**. 

> [!IMPORTANT]
> **Estado del Negocio**: He actualizado el estado a `demo_ready`. El script de outreach **solo contacta a los negocios que tienen la demo lista**. Si está en `pending`, el script dirá que hay 0 prospectos.

## 2. Paso 1: Generación y Despliegue (YA REALIZADO PARA TEST)
He preparado el CSV para que puedas saltar directamente al envío de WhatsApp. Si quieres añadir más, usa este comando:

```bash
python3 src/automate.py --csv data/test_business.csv --limit 1
```

## 3. Paso 2: Envío de Outreach (WhatsApp) - ¡LISTO PARA PROBAR!
He simplificado los iconos para que se vean mejor en todos los terminales y clientes.

```bash
# Prueba el Dry Run ahora (debería encontrar 1 prospecto)
python3 src/messaging/bulk_outreach.py --csv data/test_business.csv --limit 1 --dry-run

# Envío real (recuerda tener el bridge activo)
python3 src/messaging/bulk_outreach.py --csv data/test_business.csv --limit 1
```

## 4. Paso 3: Simulación de Respuesta de IA
Para probar cómo contestaría el bot a un cliente interesado, puedes usar el script de procesamiento de entrada.

```bash
python3 src/messaging/process_incoming.py "+34622795058" "Hola, me gusta la web. ¿Qué precio tiene el dominio propio?"
```

## 5. Control de Estados
Puedes ver cómo evoluciona el estado del negocio en el CSV:
- `pending`: Inicial
- `demo_ready`: Web generada y desplegada.
- `contacted`: Mensaje de WhatsApp enviado.

---
¿Quieres que ejecute yo el **Paso 1** ahora mismo para empezar la prueba?
