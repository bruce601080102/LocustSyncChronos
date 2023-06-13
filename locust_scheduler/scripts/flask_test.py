from locust import FastHttpUser, task


test_data = {"name": "test111"}


class QuickstartUser(FastHttpUser):

    @task()
    def on_start(self):
        with self.client.post(":9999/form", json=test_data, headers={'Content-type': 'application/json'}, catch_response=True) as ts:
            if ts.status_code == 200:
                ts_js = ts.json()
                if ts_js["name"] == test_data["name"]:
                    ts.success()
            else:
                ts.failure("post failed")
