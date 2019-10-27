import pickle
from redis import Redis as _Redis

from swiper.cfg import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=None, xx=False):
        pickled_data = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickled_data, ex, px, nx, xx)

    def get(self,name,default=None):
        pickled_data=super().get(name)
        if pickled_data is None:
            return default
        else:
            try:
                return  pickle.loads(pickled_data)
            except(TypeError,pickle.UnpicklingError):
                return pickled_data

rds = REDIS(**REDIS)
