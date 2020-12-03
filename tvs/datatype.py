class PtrDetails:
    def __init__(self, region, ptr):
        self.region = region
        self.ptr = ptr


class UserStatusDetail:
    def __init__(self, status, reason,location, school,ward,length):
        self.status = status
        self.reason = reason
        self.location = location
        self.school = school
        self.ward = ward
        self.length = length

class ToMap:
    def __init__(self, reg, p):
        self.reg = reg
        self.p = p

class ToMap1:
    def __init__(self, data_pair):
        self.data_pair=data_pair