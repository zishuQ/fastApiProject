from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, joinedload
from mysqlite.models import Base
from mysqlite.models import Defect, ProductLine, TireInfo, DefectInfo


class SqliteOption():
    def __init__(self, db_path: str = 'tire.db'):
        self.engine = create_engine('sqlite:///' + db_path, echo=False)
        self.session_local = sessionmaker(
            bind=self.engine
        )
        self.tables = [
            Defect,
            ProductLine,
            TireInfo,
            DefectInfo
        ]

    def __enter__(self):
        with self.engine.connect() as conn:
            for table in self.tables:
                if not inspect(conn).has_table(table.__tablename__):
                    Base.metadata.create_all(self.engine)
        self.session = self.session_local()
        self.Defect_initialize()
        self.ProductLine_initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def Defect_initialize(self):
        defects_list = [
            'blister',
            'impurity',
            'taiti_xixian',
            'taiti_kaigen',
            'taiti_jiaocha',
            'daishuceng_kaigen',
            'daishuceng_chaji',
            '0_degree_sanxian',
            'dangangsi_wanqu',
            'daishuceng_dajie',
            'undefined'
        ]
        existing_defect = self.session.query(
            Defect).filter_by(DefectNo=1).first()
        if existing_defect:
            return
        for i, v in enumerate(defects_list):
            defect = Defect(
                DefectNo=i + 1,
                DefectName=v
            )
            self.session.add(defect)
        self.session.commit()

    def ProductLine_initialize(self):
        product_lines = [
            '1号',
            '2号',
            '3号',
            '4号',
            '5号'
        ]
        existing_product_line = self.session.query(
            ProductLine).filter_by(LineNo=1).first()
        if existing_product_line:
            return
        for i, v in enumerate(product_lines):
            product_line = ProductLine(
                LineNo=i + 1,
                LineName=v
            )
            self.session.add(product_line)
        self.session.commit()

    def merge_tire_info(self, data):
        existing_tire = self.session.query(
            TireInfo).filter_by(TireName=data.get('TireName')).first()
        if existing_tire:
            existing_tire.ProduceDate = data.get('ProduceDate')
        else:
            tire_info = TireInfo(
                LineNo=data.get('LineNo'),
                TireName=data.get('TireName'),
                ProduceDate=data.get('ProduceDate')
            )
            self.session.add(tire_info)
        self.session.commit()

    def merge_detect_info(self, data):
        existing_detect = self.session.query(
            DefectInfo).filter_by(
            TireName=data.get('TireName')).first()
        if existing_detect:
            existing_detect.Info = data.get('Info')
            existing_detect.DefectDate = data.get('DefectDate')
        else:
            defect_info = DefectInfo(
                TireName=data.get('TireName'),
                Info=data.get('Info'),
                DefectDate=data.get('DefectDate')
            )
            self.session.add(defect_info)
        self.session.commit()

    def select_detect_info(self, LineNo: str):
        result = self.session.query(
            ProductLine.LineNo,
            TireInfo.TireName,
            TireInfo.ProduceDate,
            DefectInfo.DefectDate,
            DefectInfo.Info
        ).join(TireInfo, ProductLine.LineNo == TireInfo.LineNo).\
            outerjoin(DefectInfo, TireInfo.TireName == DefectInfo.TireName).\
            filter(ProductLine.LineNo == LineNo).all()
        return result
