# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
from website.models import CandidatesScheduleObj
# ------------------------ imports end ------------------------

def function_run():
    localhost_print_function('00-function_run start')
    var1 = 'expire_15e186a3-2ff5-42ec-a4c5-e4fd353d7fb9'
    schedule_obj = CandidatesScheduleObj.query.filter_by(fk_stripe_price_id=var1).first()
    if schedule_obj != None and schedule_obj != []:
        schedule_obj.candidate_status = 'Past Due'
        db.session.commit()
    localhost_print_function('01-function_run end')


if __name__ == '__main__':
    function_run()
