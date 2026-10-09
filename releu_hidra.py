from psie_kernel import kernel_arca
import requests

class ReleuHidraAPI:
    def explain_alarm(self, alarm_id: str, topology: dict, telemetry: list):
        lectie = {
            "original": f"Alarma {alarm_id} declansata",
            "imbunatatire": f"Explicatie cu topology {topology} + telemetry {len(telemetry)} readings",
            "intrebare": "Cum explici trilingv Ar/Fr/En fara sa inventezi fizica?"
        }
        verdict = kernel_arca(lectie)
        if verdict.status != "APROBAT_VOT":
            return verdict

        # cheama Java, nu scrie direct in DB
        resp = requests.post("http://hidra-api:8080/api/v1/intelligence/explain",
                             json={"alarmId": alarm_id, "evidence": verdict.evidence})
        return resp.json()
