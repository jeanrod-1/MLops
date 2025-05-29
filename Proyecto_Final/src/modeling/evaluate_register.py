"""
Selecciona el run con mejor F1 y lo move a 'Production'.
"""
import mlflow
from mlflow.tracking import MlflowClient
from config import MLFLOW_TRACKING_URI

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()
    model_name = 'house_prices_model'

    experiment = client.get_experiment_by_name("house-prices-v1")
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.mae ASC"])
    best_run = runs[0]

    model_versions = client.search_model_versions(f"name='{model_name}'")
    
    # Archiva cualquier modelo en producción
    for mv in model_versions:
        if mv.current_stage == "Production":
            client.transition_model_version_stage(model_name, mv.version, "Archived")

    # Intenta encontrar versión del modelo con el run_id del best_run
    try:
        matching_version = next(mv.version for mv in model_versions if mv.run_id == best_run.info.run_id)
        print(f"Versión encontrada para el mejor run: {matching_version}")
    except StopIteration:
        # Fallback: usa la última versión disponible
        if model_versions:
            matching_version = sorted(model_versions, key=lambda mv: int(mv.version))[-1].version
            print(f"No se encontró versión para el mejor run. Usando versión fallback: {matching_version}")
        else:
            raise ValueError("No hay versiones registradas del modelo 'diabetes_rf'.")

    # Promueve el modelo
    client.transition_model_version_stage(
        name=model_name,
        version=matching_version,
        stage="Production",
        archive_existing_versions=False,
    )

    # Registrar que fue promovido
    client.set_tag(best_run.info.run_id, "production_status", "promoted_to_production")
    
    print("Modelo promovido a Producción.")

if __name__ == "__main__":
    main()