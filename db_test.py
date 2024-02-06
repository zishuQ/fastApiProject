from mysqlite.sqlite_option import SqliteOption
from mysqlite.models import *

if __name__ == '__main__':
    with SqliteOption() as sqlite_option:
        result = sqlite_option.session.query(Defect).all()
        for defect in result:
            print(defect.DefectNo, defect.DefectName)
        print('------------------')
        result = sqlite_option.session.query(ProductLine).all()
        for line in result:
            print(line.LineNo, line.LineName)
        print('------------------')
        result = sqlite_option.session.query(TireInfo).all()
        for tire in result:
            print(tire.TireNo, tire.LineNo, tire.TireName, tire.ProduceDate)
        print('------------------')
        result = sqlite_option.session.query(DefectInfo).all()
        for defect in result:
            print(defect.id, defect.TireName, defect.Info, defect.DefectDate)
        print('------------------')
        result = sqlite_option.select_detect_info(1)
        for val in result:
            for i in val:
                print(i)
            break