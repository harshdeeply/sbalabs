from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class ReportService(Base):
    """ Report Service Location """

    __tablename__ = "report_service"

    id = Column(Integer, primary_key=True)
    businessID = Column(String(250), nullable=False)
    serviceOffered = Column(String(250), nullable=False)
    openingHours = Column(String(100), nullable=False)
    closingHours = Column(String(100), nullable=False)
    phoneNumber = Column(String(100), nullable=False)
    streetNumber = Column(String(250), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postalCode = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(
        self,
        businessID,
        serviceOffered,
        openingHours,
        closingHours,
        phoneNumber,
        streetNumber,
        city,
        province,
        country,
        postalCode,
    ):
        """ Initializes a report service reading """
        self.businessID = businessID
        self.serviceOffered = serviceOffered
        self.openingHours = openingHours
        self.closingHours = closingHours
        self.date_created = (
            datetime.datetime.now()
        )  # Sets the date/time record is created
        self.phoneNumber = phoneNumber
        self.streetNumber = streetNumber
        self.city = city
        self.province = province
        self.country = country
        self.postalCode = postalCode

    def to_dict(self):
        """ Dictionary Representation of a report service reading """
        dict = {}
        dict["id"] = self.id
        dict["businessID"] = self.businessID
        dict["serviceOffered"] = self.serviceOffered
        dict["streetAddress"] = {}
        dict["streetAddress"]["streetNumber"] = self.streetNumber
        dict["streetAddress"]["city"] = self.city
        dict["streetAddress"]["province"] = self.province
        dict["streetAddress"]["country"] = self.country
        dict["streetAddress"]["postalCode"] = self.postalCode
        dict["openingHours"] = self.openingHours
        dict["closingHours"] = self.closingHours
        dict["phoneNumber"] = self.phoneNumber
        dict["date_created"] = self.date_created

        return dict
