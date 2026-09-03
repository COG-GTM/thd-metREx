import json
import secrets
import unittest

from ..base import BaseTestCase


API_KEY_HEADERS = {'X-API-Key': 'test-scheduler-api-key'}


def get_info(client):
    return client.get(
        '/scheduler',
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


def get_job(client, job_id):
    return client.get(
        '/scheduler/jobs/' + job_id,
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


def get_jobs(client):
    return client.get(
        '/scheduler/jobs',
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


def pause_job(client, job_id):
    return client.post(
        '/scheduler/jobs/' + job_id + '/pause',
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


def resume_job(client, job_id):
    return client.post(
        '/scheduler/jobs/' + job_id + '/resume',
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


def run_job(client, job_id):
    return client.post(
        '/scheduler/jobs/' + job_id + '/run',
        content_type='application/json',
        headers=API_KEY_HEADERS
    )


class TestSchedulerBlueprint(BaseTestCase):
    def test_get_info_without_api_key_is_rejected(self):
        response = self.client.get('/scheduler')

        self.assertEqual(response.status_code, 401)

    def test_get_info_with_wrong_api_key_is_rejected(self):
        response = self.client.get(
            '/scheduler',
            headers={'X-API-Key': 'wrong'}
        )

        self.assertEqual(response.status_code, 401)

    def test_bearer_token_is_accepted(self):
        response = self.client.get(
            '/scheduler',
            headers={'Authorization': 'Bearer test-scheduler-api-key'}
        )

        self.assertEqual(response.status_code, 200)

    def test_run_job_via_get_is_not_allowed(self):
        response = get_jobs(self.client)

        jobs = json.loads(response.data)

        if jobs:
            job_id = jobs[secrets.randbelow(len(jobs))]['id']

            response = self.client.get(
                '/scheduler/jobs/' + job_id + '/run',
                headers=API_KEY_HEADERS
            )

            self.assertEqual(response.status_code, 405)

    def test_scheduler_api_disabled_without_key(self):
        original_api_key = self.app.config.get('SCHEDULER_API_KEY')
        self.app.config['SCHEDULER_API_KEY'] = None

        try:
            response = self.client.get(
                '/scheduler',
                headers=API_KEY_HEADERS
            )

            self.assertEqual(response.status_code, 503)
        finally:
            self.app.config['SCHEDULER_API_KEY'] = original_api_key

    def test_get_info(self):
        with self.client:
            response = get_info(self.client)

            info = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(info['running'])

    def test_get_job(self):
        with self.client:
            response = get_jobs(self.client)

            jobs = json.loads(response.data)

            total_jobs = len(jobs)

            if total_jobs:
                job_id = jobs[secrets.randbelow(total_jobs)]['id']

                response = get_job(self.client, job_id)

                job = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(job['id'], job_id)

    def test_get_jobs(self):
        with self.client:
            response = get_jobs(self.client)

            self.assertEqual(response.status_code, 200)

    def test_pause_job(self):
        with self.client:
            response = get_jobs(self.client)

            jobs = json.loads(response.data)

            total_jobs = len(jobs)

            if total_jobs:
                job_id = jobs[secrets.randbelow(total_jobs)]['id']

                response = pause_job(self.client, job_id)

                job = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(job['id'], job_id)

                if 'next_run_time' in job.keys():
                    self.assertIsNone(job['next_run_time'])

    def test_resume_job(self):
        with self.client:
            response = get_jobs(self.client)

            jobs = json.loads(response.data)

            total_jobs = len(jobs)

            if total_jobs:
                job_id = jobs[secrets.randbelow(total_jobs)]['id']

                response = resume_job(self.client, job_id)

                job = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(job['id'], job_id)

                if 'next_run_time' in job.keys():
                    self.assertIsNotNone(job['next_run_time'])

    def test_run_job(self):
        with self.client:
            response = get_jobs(self.client)

            jobs = json.loads(response.data)

            total_jobs = len(jobs)

            if total_jobs:
                job_id = jobs[secrets.randbelow(total_jobs)]['id']

                response = run_job(self.client, job_id)

                job = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(job['id'], job_id)


if __name__ == '__main__':
    unittest.main()
