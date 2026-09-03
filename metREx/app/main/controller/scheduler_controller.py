from flask_restx import Resource

from flask_apscheduler import api as aps_api

from ..util.dto import SchedulerDto
from ..util.flask_helper import require_api_key

api = SchedulerDto.api


@api.route('')
class Scheduler(Resource):
    @api.doc('get_scheduler_info', security='apikey')
    @require_api_key
    def get(self):
        """Gets the scheduler info."""
        return aps_api.get_scheduler_info()


@api.route('/jobs')
class SchedulerJobList(Resource):
    @api.doc('get_jobs', security='apikey')
    @require_api_key
    def get(self):
        """Gets all scheduled jobs."""
        return aps_api.get_jobs()

    # @api.doc('add_job')
    # def post(self):
    #     """Adds a new job."""
    #     return aps_api.add_job()


@api.route('/jobs/<job_id>')
class SchedulerJob(Resource):
    @api.doc('get_job', security='apikey')
    @require_api_key
    def get(self, job_id):
        """Gets a job."""
        return aps_api.get_job(job_id)

    # @api.doc('delete_job')
    # def delete(self, job_id):
    #     """Deletes a job."""
    #     return aps_api.delete_job(job_id)

    # @api.doc('update_job')
    # def patch(self, job_id):
    #     """Updates a job."""
    #     return aps_api.update_job(job_id)


@api.route('/jobs/<job_id>/pause')
class SchedulerJobPause(Resource):
    @api.doc('pause_job', security='apikey')
    @require_api_key
    def post(self, job_id):
        """Pauses a job."""
        return aps_api.pause_job(job_id)


@api.route('/jobs/<job_id>/resume')
class SchedulerJobResume(Resource):
    @api.doc('resume_job', security='apikey')
    @require_api_key
    def post(self, job_id):
        """Resumes a job."""
        return aps_api.resume_job(job_id)


@api.route('/jobs/<job_id>/run')
class SchedulerJobRun(Resource):
    @api.doc('run_job', security='apikey')
    @require_api_key
    def post(self, job_id):
        """Runs a job."""
        return aps_api.run_job(job_id)
