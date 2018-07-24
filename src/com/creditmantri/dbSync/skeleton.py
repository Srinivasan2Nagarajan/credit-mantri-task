#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.py:

    [console_scripts]
    fibonacci = dbSync.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

"""
from __future__ import division, print_function, absolute_import

import sys
import logging
from com.creditmantri.dbSync import __version__
import json
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

__author__ = "Srinivasan Nagaraja Rao"
__copyright__ = "Srinivasan Nagaraja Rao"
__license__ = "mit"

_logger = logging.getLogger(__name__)

# Spark Context created here
sc = SparkContext("local[*]", appName="creditMantri")

# Spark Streaming Context Created Here
ssc = StreamingContext(sc, 1)
topic = "credit-mantri"
brokers = "localhost:9092"
kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})


def convert(rdd):
    df_json = rdd.map(lambda x: json.loads(x[1])).toDF()
    return df_json


def write_mongo(rdd):
    try:
        convert(rdd).write \
            .format('com.mongodb.spark.sql.DefaultSource').mode('append') \
            .option('database', 'NAME').option('collection', 'COLLECTION_MONGODB').save()
    except:
        pass


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    convert(kvs)


def run():
    """Entry point for console_scripts
    """
    main()


if __name__ == "__main__":
    run()
