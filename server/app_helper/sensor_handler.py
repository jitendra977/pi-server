from server.models import SensorData

class SensorReader:
    def __init__(self, sensor_name=None, sensor_type=None):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type

    def get_sensor_data(self):
        query = SensorData.objects.all()

        if self.sensor_name:
            query = query.filter(sensor_name=self.sensor_name)
        
        if self.sensor_type:
            query = query.filter(sensor_type=self.sensor_type)

        return query

    def read_latest_sensor_data(self):
        return self.get_sensor_data().order_by('-timestamp').first()

    def read_all_sensor_data(self):
        return list(self.get_sensor_data())