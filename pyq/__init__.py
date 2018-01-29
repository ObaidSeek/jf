import regex as re
import sys
import json
import logging
from dateutil import parser as dateutil
from datetime import datetime, timezone
import dateparser
from functools import reduce
FORMAT = '%(levelname)s %(name)s : %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)


namere = re.compile(r'([{,] *)([^{} "\',]+):')
makexre = re.compile('([ (])(\.[a-zA-Z])')
#indented_str = '(\([^()]*(?1)?\))'
#lambdare = re.compile("([a-zA-Z][^() ,]+)\(([^()]*("+indented_str+"?[^()]*)+)\)")
lambdare = re.compile("([a-zA-Z][^() ,]+)(\([^()]*((?2)?[^()]*)+\))")
nowre = re.compile("NOW\(\)")

#age = lambda x: datetime.now() - dateparser.parse(x)
def age(x):
    logger.debug("Calculating the age of '%s'", x)
    ret = 0
    try:
        ret = datetime.now() - dateparser.parse(str(x))
    except:
        ret = datetime.now(timezone.utc) - dateparser.parse(str(x))
    logger.debug("Age of '%s' is %s", x, repr(ret))
    return ret

#parse_timedelta = lambda x: datetime.now() - dateparser.parse(x)

def parse_value(v):
#  logger.debug("Parsing: '%s'", v)
  try:
    if len(v) > 10:
      time = dateutil.parse(v)
    else:
      return v
    #time = dateparser.parse(v)
#    logger.info("Found a timestamp: %s", v)
    return time
  except:
    return v

class Struct:
  def __init__(self, **entries):
    for k, v in entries.items():
      if type(v) in (list, dict):
        self.__dict__[k] = to_struct(v)
      else:
        self.__dict__[k] = parse_value(v)
  def __getitem__(self, item):
    return self.__dict__[item]

def to_struct(v):
  if type(v) == dict:
    return Struct(**v)
  if type(v) == list:
    return [to_struct(a) for a in v]
  return v

toStruct = lambda arr: map(to_struct, arr)

class StructEncoder(json.JSONEncoder):
  def default(self, o):
    try:
      return o.__dict__
    except:
      return o.__str__()

class genProcessor:
  def __init__(self, igen, filters=[]):
    self.igen = igen
    self._filters = filters
  def process(self):
    pipeline = self.igen
    for f in self._filters:
      pipeline = f(toStruct(pipeline))
    return pipeline

def run_query(query, data, sort_keys=False):
  logger.debug(query)
  query = namere.sub(r'\1"\2":', query)
  logger.debug(query)
  query = makexre.sub(r'\1x\2', query)
  logger.debug(query)
  query = lambdare.sub(r'lambda arr: \1(lambda x, *rest: \2, arr)', query)
  logger.debug(query)
  query = nowre.sub(r'datetime.now(timezone.utc)', query)
  logger.debug(query)
  query = "gp(x, [" + query + "]).process()" #Make it a list
  logger.debug(query)
  globalscope = {
      "x": data,
      "gp": genProcessor,
      "age": age,
      "reduce": reduce,
      "datetime": datetime,
      "timezone": timezone}
  for it in eval(query, globalscope):
    yield it


if __name__ == "__main__":
  inq = (json.loads(d) for d in sys.stdin)
  for out in run_query(sys.argv[1], inq):
    print(json.dumps(out, cls=StructEncoder))
