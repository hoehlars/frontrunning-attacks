from datetime import datetime, date


class InsertionAtkLiveDAO():
    def __init__(self):
        self.counter = 0
        pass

    def get_live_transactions(self):
        self.counter += 1
        today = date.today()
        formatted_date = today.strftime('%d %B, %Y')
        current_time = datetime.now().strftime('%H:%M:%S')
        return [
            {
                'index': self.counter,
                'date': str(formatted_date),
                'time': current_time,
                'transactionHash': 123,
                'type': 'Attack',
                'gasPrice': 100,
                'ethTransferred': 10
            },
            {
                'index': self.counter+1,
                "date": str(formatted_date),
                'time': current_time,
                'transactionHash': 123,
                'type': 'Normal',
                'gasPrice': 100,
                'ethTransferred': 10
            }, {
                'index': self.counter+2,
                "date": str(formatted_date),
                'time': current_time,
                'transactionHash': 123,
                'type': 'Normal',
                'gasPrice': 100,
                'ethTransferred': 10
            },
            {
                'index': self.counter+3,
                "date": str(formatted_date),
                'time': current_time,
                'transactionHash': 123,
                'type': 'Normal',
                'gasPrice': 100,
                'ethTransferred': 10
            },
            {
                'index': self.counter+4,
                "date": str(formatted_date),
                'time': current_time,
                'transactionHash': 123,
                'type': 'Normal',
                'gasPrice': 100,
                'ethTransferred': 10
            }
        ]
