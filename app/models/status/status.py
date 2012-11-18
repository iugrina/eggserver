import datetime

from common import egg_errors
from common.utils import ExceptionLogger

class Status(ExceptionLogger):
    """Mangle with statuses (speech bubble)"""

    def __init__(self, db, logging_file=None):
        self.db = db
        self.identifier = "Status class"
        self.lf = logging_file

    def get_statuses(self, user_id):
        try:
            s = self.db.StatusModel.find({'user_id' : user_id})[0]
            if not s :
                raise egg_errors.UnknownUserIDException
            return s['statuses']
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def get_last_status(self, user_id):
        try:
            s = self.db.StatusModel.find({'user_id' : user_id})[0]
            if not s :
                raise egg_errors.UnknownUserIDException
            return {'last_status': s['last_status'], 'last_status_id': s['last_status_id'], 'datetime': s['last_status_datetime'] }
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def add_status(self, user_id, status):
        try:
            sp = self.db.StatusModel.find_one({'user_id' : user_id})
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

        if not sp :
            raise egg_errors.UnknownUserIDException

        statuses = sp['statuses']
        date = datetime.datetime.utcnow()

        statuses.append({'status_id': sp['last_status_id']+1,
                         'status': unicode(status),
                         'datetime': date })

        sp['statuses'] = statuses
        sp['last_status_id'] = sp['last_status_id']+1
        sp['last_status'] = unicode(status)
        sp['last_status_datetime'] = date

        try:
            sp.save()
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def delete_status(self, user_id, status_id):
        try:
            sp = self.db.StatusModel.find_one({'user_id' : user_id})
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

        if not sp :
            raise egg_errors.UnknownUserIDException

        statuses = sp['statuses']
        l = len(statuses)

        if 1 == l :
            raise egg_errors.LastStatusDeleteException

        new_last_id = -1
        del_ind = -1
        for ind in range(0, l):
            if statuses[ind]['status_id'] == status_id :
                del_ind = ind
                continue
            
            if statuses[ind]['status_id'] > new_last_id :
                new_last_id = statuses[ind]['status_id']
                new_last_status = statuses[ind]['status']
                new_last_datetime = statuses[ind]['datetime']

        if del_ind == -1 :
            raise egg_errors.UnknownStatusIDException
        else :
            del statuses[del_ind]
                
        try:
            sp['last_status'] = new_last_status
            sp['last_status_id'] = new_last_id
            sp['last_status_datetime'] = new_last_datetime
            sp['statuses'] = statuses
            sp.save()
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible


