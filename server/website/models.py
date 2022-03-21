from . import db


class Company(db.Model):
    __tablename__ = 'Company'

    CompID = db.Column(db.INTEGER, primary_key=True)
    CompanyName = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    Password = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    Email = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    Logo = db.Column(db.String, nullable=False)
    GeneralIndustry = db.Column(db.VARCHAR(255), nullable=False)
    Bio = db.Column(db.TEXT, nullable=False)

    CompanyContracts = db.relationship('Contracts')
    BlockedDev = db.relationship('Blocked')


class Developers(db.Model):
    __tablename__ = 'Developers'

    DevID = db.Column(db.INTEGER, primary_key=True)
    Username = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    Email = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    Password = db.Column(db.VARCHAR(255), nullable=False)
    UserAvatar = db.Column(db.VARCHAR(255), nullable=False)
    Status = db.Column(db.VARCHAR(255), nullable=False)
    Experience = db.Column(db.TEXT, nullable=False)

    ContractsApplied = db.relationship('Applications')
    ExpDeveloper = db.relationship('Experience')
    BlockedComp = db.relationship('Blocked')


class Contracts(db.Model):
    __tablename__ = 'Contracts'

    ContractID = db.Column(db.INTEGER, primary_key=True)
    Length = db.Column(db.VARCHAR(255), nullable=False)
    Location = db.Column(db.VARCHAR(255), nullable=False)
    DatePost = db.Column(db.DATE, nullable=False)
    Value = db.Column(db.FLOAT, nullable=False)
    Descript = db.Column(db.String, nullable=False)
    Status = db.Column(db.VARCHAR(255), nullable=False)

    ContractApplications = db.relationship('Applications')
    PrefLangContract = db.relationship('PrefLang')
    CompID = db.Column(db.INTEGER, db.ForeignKey('Company.CompID'))


class Applications(db.Model):
    __tablename__ = 'Applications'

    ApplyID = db.Column(db.INTEGER, primary_key=True)
    ApplyStatus = db.Column(db.VARCHAR(255), nullable=False)
    CompID = db.Column(db.INTEGER, nullable=False)

    DevID = db.Column(db.INTEGER, db.ForeignKey('Developers.DevID'))
    ContractID = db.Column(db.INTEGER, db.ForeignKey('Contracts.ContractID'))


class Experience(db.Model):
    __tablename__ = 'Experience'

    ExpID = db.Column(db.INTEGER, primary_key=True)
    Language = db.Column(db.VARCHAR(255), nullable=False)

    DevID = db.Column(db.INTEGER, db.ForeignKey('Developers.DevID'))


class PrefLang(db.Model):
    __tablename__ = 'PrefLang'

    PrefLangID = db.Column(db.INTEGER, primary_key=True)
    Language = db.Column(db.VARCHAR(255), nullable=False)

    ContractID = db.Column(db.INTEGER, db.ForeignKey('Contracts.ContractID'))


class Blocked(db.Model):
    __tablename__ = 'Blocked'

    BlockID = db.Column(db.INTEGER, primary_key=True)

    CompID = db.Column(db.INTEGER, db.ForeignKey('Company.CompID'))
    DevID = db.Column(db.INTEGER, db.ForeignKey('Developers.DevID'))
