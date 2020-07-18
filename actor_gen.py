from __future__ import print_function
from __future__ import unicode_literals
import sys
import logging
import requests
import datetime
import dateutil
import uploader
import utilities
import formatter
import postprocess
import oneaday_filter
import result_formatter
import scraper_connection


def main(file_details, geo_details, server_details, petrarch_version, run_date, mongo_details, logger_file=None, run_filter=None,
         version=''):
    """
    Main function to run all the things.

    Parameters
    ----------

    file_details: Named tuple.
                    All the other config information not in ``server_details``.

    geo_details: Named tuple.
                  Settings for geocoding.

    server_details: Named tuple.
                    Config information specifically related to the remote
                    server for FTP uploading.

    petrarch_version: String.
                       Which version of Petrarch to use. Must be '1' or '2'

    logger_file: String.
                    Path to a log file. Defaults to ``None`` and opens a
                    ``PHOX_pipeline.log`` file in the current working
                    directory.

    run_filter: String.
                Whether to run the ``oneaday_formatter``. Takes True or False
                (strings) as values.

    run_date: String.
                Date of the format YYYYMMDD. The pipeline will run using this
                date. If not specified the pipeline will run with
                ``current_date`` minus one day.
    """
    if logger_file:
        utilities.init_logger(logger_file)
    else:
        utilities.init_logger('PHOX_pipeline.log')
    # get a local copy for the pipeline
    logger = logging.getLogger('pipeline_log')

    if petrarch_version == '1':
        from petrarch import petrarch
        logger.info("Using original Petrarch version")
    elif petrarch_version == '2':
        from petrarch2 import petrarch2 as petrarch
        logger.info("Using Petrarch2")
    else:
        logger.error("Invalid Petrarch version. Argument must be '1' or '2'")


    print('\nPHOX.pipeline run:', datetime.datetime.utcnow())

    if run_date:
        process_date = dateutil.parser.parse(run_date)
        date_string = '{:02d}{:02d}{:02d}'.format(process_date.year,
                                                  process_date.month,
                                                  process_date.day)
        logger.info('Date string: {}'.format(date_string))
        print('Date string:', date_string)
    else:
        process_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        date_string = '{:02d}{:02d}{:02d}'.format(process_date.year,
                                                  process_date.month,
                                                  process_date.day)
        logger.info('Date string: {}'.format(date_string))
        print('Date string:', date_string)
    results, scraperfilename = scraper_connection.main(process_date,
                                                       file_details)
    if geo_details.geo_service == "Mordecai":
        dest = "{0}:{1}/places".format(geo_details.mordecai_host, geo_details.mordecai_port)
        try:
            out = requests.get(dest)
            assert out.status_code == 200
        except (AssertionError, requests.exceptions.ConnectionError):
            print("Mordecai geolocation service not responding. Continuing anyway...")
    elif geo_details.geo_service == "CLIFF":
        print("CLIFF")
    else:
        print("Invalid geo service name. Must be 'CLIFF' or 'Mordecai'. Continuing...")


    if scraperfilename:
        logger.info("Scraper file name: " + scraperfilename)
        print("Scraper file name:", scraperfilename)

    logger.info("Running Mongo.formatter.py")
    print("Running Mongo.formatter.py")
    formatted = formatter.main(results, file_details,
                               process_date, date_string)
    logger.info("Running PETRARCH")
    file_details.fullfile_stem + date_string
    
    print('Running PETRARCH in Null Actors Mode.')
    # DGM Run this in actor-gen mode
    ACTOR_OUTPUT_FILE = "events_null_actors_mode_" + run_date + ".txt"
    petrarch.run_pipeline(formatted, out_file = ACTOR_OUTPUT_FILE, config = "petr_config.ini", write_output=True,
                                             parsed=True)

    print("See events results in: " + ACTOR_OUTPUT_FILE)   
    print("See actors list in: nullactors." + ACTOR_OUTPUT_FILE)
    logger.info('PHOX.pipeline end')
    print('PHOX.pipeline end:', datetime.datetime.utcnow())


def run():
    #server_details, geo_details, file_details, petrarch_version, run_date = utilities.parse_config('PHOX_config.ini')
    cfg = utilities.parse_config('PHOX_config.ini')
    main(cfg['file_list'], cfg['geo_list'], cfg['server_list'], 
         cfg['petrarch_version'], cfg['run_date'], cfg['file_list'].log_file,
         run_filter=cfg['file_list'].oneaday_filter, version='v0.0.0')

if __name__ == '__main__':
    run()
