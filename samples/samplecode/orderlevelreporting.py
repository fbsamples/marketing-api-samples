# Copyright (c) 2016-present, Facebook, Inc. All rights reserved.
#
# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.
#
# As with any software that integrates with the Facebook platform, your use of
# this software is subject to the Facebook Developer Principles and Policies
# [http://developers.facebook.com/policy/]. This copyright notice shall be
# included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
# Order Level Reporting

## Retrieving order level reporting from the API.

***

This sample shows how to retrieve order level reports for a specific pixel
and/or app ID within one of your business managers.

Downloads here will timeout after 5 mins and should only be used for small
data-sets.
"""
import itertools
import logging
import Queue
import sys
import threading
from datetime import date, datetime, time, timedelta
from facebookads.api import FacebookAdsApi

logger = logging.getLogger(__name__)

# FacebookAdsApi.init(
#    app_id = '<SERVER_APP_ID>',
#    access_token = '<USER_ACCESS_TOKEN>',
# )

class OrderLevelReportingSample:
    """
    The main sample class.
    """

    def retrieve_order_level_report_data_parallel(
        self,
        from_date,
        to_date,
        business_id,
        pixel_id='',
        app_id='',
        splits=4,
    ):
        """
          Parallelise the retrieval of order level reports.
        """
        d = (to_date - from_date) / splits

        # Convert any dates to datetime before splitting
        # otherwise we lose intra-day resolution
        start_time = from_date

        if isinstance(start_time, date):
            start_time = datetime.combine(start_time, time())

        time_partitions = [
            (i * d + start_time, (i + 1) * d + start_time)
            for i in range(splits)
        ]

        # keep a copy of the Ads API session as we're going to be using
        # it across new threads
        api = FacebookAdsApi.get_default_api()

        return itertools.chain.from_iterable(
            map(
                lambda (start, end): self.zzz_buffer_iterable_async(
                    # promise fetches time-ranges concurrently
                    self.retrieve_order_level_report_data(
                        api=api,
                        from_date=start,
                        to_date=end,
                        business_id=business_id,
                        pixel_id=pixel_id,
                        app_id=app_id,
                    ),
                    buffer_size=30,
                ),
                time_partitions,
            )
        )

    def retrieve_order_level_report_data(
        self,
        from_date,
        to_date,
        business_id,
        pixel_id,
        app_id,
        limit=150,
        api=None,
    ):
        """
          Retrieve order level reporting for a given time range.
        """
        path = (business_id, "order_id_attributions", )
        params = {
            'since': from_date.strftime('%s'),
            'until': to_date.strftime('%s'),
            'pixel_id': pixel_id,
            'app_id': app_id,
            'limit': limit,
        }

        if not api:
            api = FacebookAdsApi.get_default_api()

        page_index = 0
        while path:
            page_index += 1

            logger.info(
                "Pulling page %s for %s/%s from %s -> %s",
                page_index, pixel_id, app_id, from_date, to_date,
            )

            response = api.call(
                FacebookAdsApi.HTTP_METHOD_GET,
                path,
                params,
            ).json()

            # only emit non-empty pages
            if response['data']:
                yield response['data']

            if 'paging' in response and 'next' in response['paging']:
                path = response['paging']['next']
                params = {}
            else:
                break

    def zzz_buffer_iterable_async(self, iterable, buffer_size=100, daemon=True):
        """
          Helper function for buffering blocking iterables on a worker thread.
        """

        YIELD = 0
        RAISE = 1
        BREAK = 2

        def iterate(iterable, thread_state, buffer):
            try:
                for el in iterable:
                    buffer.put((YIELD, el,))
                    if thread_state.get(BREAK):
                        break
            except Exception, e:
                buffer.put((RAISE, e, sys.exc_info()[2],))
            else:
                buffer.put((BREAK,))

        buffer = Queue.Queue(maxsize=buffer_size)
        thread_state = dict()

        t = threading.Thread(
            target=iterate,
            args=(iterable, thread_state, buffer),
        )
        t.daemon = daemon
        t.start()

        def iterator():
            try:
                for signal in iter(buffer.get, (BREAK,)):
                    if signal[0] == YIELD:
                        yield signal[1]
                    elif signal[0] == RAISE:
                        raise signal[1], None, signal[2]
            finally:
                thread_state[BREAK] = True
                while buffer.full():
                    buffer.get_nowait()
                t.join()

        return iterator()

if __name__ == '__main__':
    import argparse
    import csv

    def convert_to_date(s):
        try:
            if s == argparse.SUPPRESS:
                return argparse.SUPPRESS
            return datetime.strptime(s, '%Y-%m-%d')
        except ValueError:
            msg = 'Not a valid YYYY-MM-DD date: "{0}"'.format(s)
            raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser(
        description='Retrieve order level attribution information from the '
                    'Facebook API and write it to STDOUT. Provide a single '
                    'date to fetch attributions for any orders from that '
                    'date. Provide two dates to pull order-level attribution '
                    'information for a date-range.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-p', type=int, required=False, dest='pixel_id',
        help='provide the FB pixel ID that order ID data was sent to',
    )
    parser.add_argument(
        '-a', type=int, required=False, dest='app_id',
        help='provide the FB app ID that order ID data was sent to',
    )
    parser.add_argument(
        '-x', '--explode', action='store_true',
        help='explode out attributions column into separate rows',
    )
    parser.add_argument(
        '-f', default='excel-tab', dest='format', choices=csv.list_dialects(),
        help='output format, \'excel-tab\' (tsv) or \'excel\' (csv)',
    )
    parser.add_argument(
        '-s', action='store_true', dest='skip_header',
        help='omit the very first row containing column headers',
    )
    parser.add_argument(
        '-c', type=int, default=4, dest='splits',
        help='split time range into this number of time periods and process '
             'concurrently on separate threads',
    )

    logging_levels = {
        'ERROR': logging.ERROR, 'INFO': logging.INFO, 'DEBUG': logging.DEBUG,
    }
    parser.add_argument(
        '-v', type=str.upper, dest='log_level',
        choices=logging_levels, default='ERROR',
        help='verbosity, level of logging',
    )

    parser.add_argument(
        'business_id', type=int,
        help='the Business Manager ID that the pixel & app belong to',
    )

    parser.add_argument(
        'from_date', type=convert_to_date,
        help='date to pull attributed orders [YYYY-MM-DD]',
    )
    parser.add_argument(
        'to_date', type=convert_to_date, nargs='?', default=argparse.SUPPRESS,
        help='optional end date [YYYY-MM-DD] (omit to fetch order '
             'attributions for just one day)',
    )

    args = vars(parser.parse_args())

    if not args.get('to_date'):
        args['to_date'] = args['from_date'] + timedelta(days=1)

    format = args.pop('format')
    skip_header = args.pop('skip_header')
    explode = args.pop('explode')

    logging.basicConfig(
        stream=sys.stderr,
        level=logging_levels[args.pop('log_level')],
    )

    fieldnames = [
        'order_id',
        'order_timestamp',
        'pixel_id',
        'app_id',
        'conversion_device',
        'attribution_type',
    ]

    sample = OrderLevelReportingSample()

    # This iterator will stream pages of results
    page_cursor = sample.retrieve_order_level_report_data_parallel(**args)

    # OR... we can flatten the results into a single list of records like this
    flattened_cursor = itertools.chain.from_iterable(page_cursor)

    # we choose one row per attributed interaction or one row per order
    if explode:
        flattened_cursor = itertools.chain.from_iterable(itertools.imap(
            lambda order: itertools.imap(
                lambda attr: dict(order, **attr),
                order.pop('attributions'),
            ),
            flattened_cursor,
        ))
        fieldnames.extend([
            'account_id', 'campaign_id', 'adset_id', 'ad_id', 'action_type',
            'impression_timestamp', 'click_timestamp', 'placement', 'device',
            'impression_cost', 'click_cost',
        ])
    else:
        # attributions will be output for each row as a json-encoded array
        fieldnames.append('attributions')

    # And we can then either sent to a DB or (in this case) print them out
    csv_writer = csv.DictWriter(
        sys.stdout,
        dialect=format,
        fieldnames=fieldnames,
    )

    for order_data in flattened_cursor:
        if not skip_header:
            csv_writer.writeheader()
            skip_header = True

        csv_writer.writerow(order_data)

        # cursor.execute(
        #   'INSERT INTO table VALUES (%s, %s, %s)',
        #   (order_data.order_id, order_data.pixel_id, ...),
        # )
