import argparse
import sys
import os

# Asegurar que el directorio raíz está en el path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.generator.site_generator import StaticSiteGenerator
from src.generator.directory_generator import DirectoryGenerator
from src.deployment.site_deployer import SiteDeployer
from src.crm.tracker import ProspectTracker
from src.messaging.outreach_manager import OutreachManager
from src.messaging.dashboard_generator import DashboardGenerator

def main():
    parser = argparse.ArgumentParser(description="Automatización total de la red de sitios localweb.")
    parser.add_argument("--limit", type=int, default=5, help="Número de sitios a generar.")
    parser.add_argument("--csv", type=str, default="data/amb_barcelona_sin_web_20260102_223732.csv", help="Ruta al CSV de datos.")
    parser.add_argument("--skip-deploy", action="store_true", help="Generar e indexar pero no subir a GitHub.")
    
    args = parser.parse_args()

    print("🚀 Iniciando Proceso Automatizado de Generación...")
    
    # Inicializar herramientas
    from src.crm.cleaner import DataCleaner
    cleaner = DataCleaner(args.csv)
    if cleaner.clean():
        print("✅ Datos limpiados y normalizados.")
        # Usar el archivo limpio para todo lo demás
        args.csv = "data/prospects_cleaned.csv"
    else:
        print("⚠️ Error en limpieza de datos, usando archivo original con precaución.")
        
    tracker = ProspectTracker(args.csv)
    outreach = OutreachManager()
    
    # 1. Generación de sitios
    print(f"\n📁 1/3: Generando hasta {args.limit} landing pages...")
    generator = StaticSiteGenerator(args.csv)
    
    # Procesar batch (ahora devuelve (prospect_dict, slug))
    generated_data = generator.process_batch(limit=args.limit)
    
    if not generated_data:
        print("⚠️ No se generaron nuevos sitios.")
    else:
        for prospect, slug in generated_data:
            # Actualizar CRM: demo_ready con el nuevo dominio personalizado
            demo_url = f"https://localpro.top/{slug}/"
            tracker.update_status(prospect['nombre'], 'demo_ready', demo_url=demo_url)
    
    # 2. Generación del directorio premium
    print("\n🗂️ 2/3: Actualizando el directorio central (SEO Hub)...")
    directory_gen = DirectoryGenerator(args.csv)
    directory_gen.generate(output_path="sites/index.html")
    
    # 3. Despliegue
    if args.skip_deploy:
        print("\n⏭️ 3/3: Despliegue omitido por el usuario.")
    else:
        print("\n📤 3/3: Desplegando cambios a GitHub Pages...")
        deployer = SiteDeployer()
        deployer.deploy()

    # 4. Resumen de Outreach & Dashboard
    print("\n📩 ACCIONES DE CONTACTO RECOMENDADAS (WhatsApp):")
    print("-" * 50)
    for prospect, slug in generated_data:
        wa_link = outreach.get_whatsapp_link(
            prospect['telefono'], 
            prospect['nombre'], 
            prospect['categoria'], 
            slug,
            prospect.get('ubicacion', 'su zona')
        )
        print(f"📍 {prospect['nombre']} ({prospect['categoria']})")
        print(f"   🔗 Demo: https://localpro.top/{slug}/")
        print(f"   💬 WhatsApp: {wa_link}")
        print("-" * 50)

    print("\n🖥️ Generando Panel de Control Visual...")
    dash_gen = DashboardGenerator(args.csv)
    dash_gen.generate()

    print("\n✅ ¡Proceso completado con éxito!")

if __name__ == "__main__":
    main()
