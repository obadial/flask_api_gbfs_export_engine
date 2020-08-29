from threading import Timer


class RepeatedTimer(object):
    def __init__(
        self,
        interval,
        function,
        url,
        list_elem_id,
        list_elem,
        station_data,
        history_list,
    ):
        self._timer = None
        self.interval = interval
        self.function = function
        self.url = url
        self.list_elem_id = list_elem_id
        self.list_elem = list_elem
        self.is_running = False
        self.start()
        self.return_value_list_id = []
        self.return_value_list = []
        self.station_data = station_data
        self.return_value_station_data = []
        self.return_value_history_list = []
        self.history_list = history_list

    def _run(self):
        self.is_running = False
        self.start()
        (
            self.return_value_list_id,
            self.return_value_list,
            self.return_value_station_data,
            self.return_value_history_list,
        ) = self.function(
            self.url,
            self.list_elem_id,
            self.list_elem,
            self.station_data,
            self.history_list,
        )
        self.list_elem_id = self.return_value_list_id
        self.list_elem = self.return_value_list
        self.station_data = self.return_value_station_data
        self.history_list = self.return_value_history_list

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
