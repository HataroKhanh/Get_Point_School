import requests
import re

class PointSchool:
    def __init__(self, url, sbd):
        super().__init__()
        self.url = url
        self.client = requests.session()
        self.sbd = sbd

    def regexxr(self):
        return [
            r"<td  >(.*?)</td>  ",
            r'formNumberInput">(.*?)</span>',
            r">([\d.,]+)</td>",
        ]

    def __params(self):
        return [
            ('module', 'Content.Listing'),
        ]

    def __data(self):
        return {
            'layout': 'Decl.DataSet.Detail.default',
            'service': 'Content.Decl.DataSet.Grouping.select',
            'itemId': '648ae2e68b624db4e80d1502',
            'keyword': self.sbd,
        }

    def info(self, _html):
        result = []
        for x in range(3):
            result += re.compile(self.regexxr()[x]).findall(_html)
        return result

    def method(self):
        ss = self.client.post(
            self.url,
            params=self.__params(),
            data=self.__data(),
        )
        return self.info(_html=ss.text)

if __name__ == '__main__':
    
    with open("HHA.csv", "w") as file:
        for x in range(400000, 400590):
            new = PointSchool(
                url="https://namdinh.edu.vn/",
                sbd=str(x),
            ).method()
            formatted_entries = [entry.replace(',', '.') for entry in new]
            file.write(','.join(formatted_entries) + '\n')
            print(formatted_entries)