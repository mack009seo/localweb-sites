from src.generator.directory_generator import DirectoryGenerator
gen = DirectoryGenerator("data/prospects_cleaned.csv")
gen.generate(output_path="sites/index.html")
print("Regeneration complete.")
