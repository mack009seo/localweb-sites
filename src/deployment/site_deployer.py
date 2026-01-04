import os
import subprocess
import sys

class SiteDeployer:
    def __init__(self, sites_dir="sites", repo_url="https://github.com/mack009seo/localweb-sites.git"):
        self.sites_dir = os.path.abspath(sites_dir)
        self.repo_url = repo_url
        self._load_env()
        self.pat = os.environ.get("GITHUB_PAT") # Carga el token desde variable de entorno

    def _load_env(self):
        """Carga variables desde .env si existe"""
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

    def run_command(self, cmd, cwd=None):
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando comando: {cmd}")
            print(f"Salida: {e.output}")
            print(f"Error: {e.stderr}")
            return None

    def deploy(self):
        print(f"🚀 Iniciando despliegue en: {self.repo_url}")
        
        if not os.path.exists(self.sites_dir):
            print(f"Error: La carpeta {self.sites_dir} no existe.")
            return

        # 1. Inicializar git si no existe
        git_dir = os.path.join(self.sites_dir, ".git")
        
        # Ajustar URL con token si existe
        auth_url = self.repo_url
        if self.pat:
            auth_url = self.repo_url.replace("https://", f"https://{self.pat}@")

        if not os.path.exists(git_dir):
            print("📦 Inicializando repositorio Git en 'sites/'...")
            self.run_command("git init", cwd=self.sites_dir)
            self.run_command(f"git remote add origin {auth_url}", cwd=self.sites_dir)
        else:
            # Asegurarse de que el remote es correcto
            self.run_command(f"git remote set-url origin {auth_url}", cwd=self.sites_dir)

        # 2. Configurar usuario si no está configurado (para evitar errores en entornos automatizados)
        self.run_command("git config user.name 'Antigravity Deployer'", cwd=self.sites_dir)
        self.run_command("git config user.email 'deployer@antigravity.ai'", cwd=self.sites_dir)

        # 3. Add, Commit y Push
        print("📤 Subiendo cambios a GitHub...")
        self.run_command("git add .", cwd=self.sites_dir)
        
        # Comprobar si hay algo que commitear
        status = self.run_command("git status --porcelain", cwd=self.sites_dir)
        if status:
            commit_msg = "Actualización automática de sitios: " + subprocess.check_output("date", shell=True).decode().strip()
            self.run_command(f'git commit -m "{commit_msg}"', cwd=self.sites_dir)
        else:
            print("ℹ️ Nada nuevo que commitear, procediendo a empujar cambios existentes...")

        # Intentar empujar a master (más compatible con el estado actual del repo local)
        print("Pushing to GitHub...")
        # Note: The original code used self.run_command which handles errors and returns None.
        # The new code uses subprocess.run directly with check=True, which raises an exception on error.
        # The subsequent 'if result is None' check will not behave as expected with this change.
        # To maintain similar error handling, you might want to wrap this in a try-except block
        # or use self.run_command for consistency.
        try:
            subprocess.run(["git", "push", "-u", "origin", "master"], 
                          cwd=self.sites_dir, check=True)
            result = "success" # Simulate a non-None result for the following check
        except subprocess.CalledProcessError as e:
            print(f"Error pushing to master: {e.stderr}")
            result = None # Simulate a None result for the following check
        
        if result is None:
            # Reintentar con master por si acaso (this line is now redundant if the above push failed)
            # If the intent was to try 'main' first and then 'master', the logic needs adjustment.
            # As per instruction, faithfully applying the change.
            self.run_command("git push -u origin master", cwd=self.sites_dir)

        print(f"✅ ¡Despliegue completado!")
        username = self.repo_url.split("/")[-2]
        repo_name = self.repo_url.split("/")[-1].replace(".git", "")
        print(f"🌐 Tus demos deberían estar pronto en: https://{username}.github.io/{repo_name}/")

if __name__ == "__main__":
    deployer = SiteDeployer()
    deployer.deploy()
