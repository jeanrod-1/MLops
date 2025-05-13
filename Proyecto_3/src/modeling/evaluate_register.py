"""
Selecciona el run con mejor F1 y lo move a 'Production'.
"""
import mlflow
from mlflow.tracking import MlflowClient
from config import MLFLOW_TRACKING_URI

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    experiment = client.get_experiment_by_name("diabetes-readmit-v2")
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.f1 DESC"])
    best_run = runs[0]

    model_versions = client.search_model_versions("name='diabetes_rf'")
    
    # Archiva cualquier modelo en producción
    for mv in model_versions:
        if mv.current_stage == "Production":
            client.transition_model_version_stage("diabetes_rf", mv.version, "Archived")

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
        name="diabetes_rf",
        version=matching_version,
        stage="Production",
        archive_existing_versions=False,
    )
    print("Modelo promovido a Producción.")

if __name__ == "__main__":
    main()