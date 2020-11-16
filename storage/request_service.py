from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RequestService(Base):
    """ Report Service Location """

    __tablename__ = "request_service"

    id = Column(Integer, primary_key=True)
    serviceType = Column(String(250), nullable=False)
    laundryType = Column(String(250), nullable=False)
    numberOfItems = Column(Integer, nullable=False)
    phoneNumber = Column(String(100), nullable=False)
    emailAddress = Column(String(100), nullable=False)
    streetNumber = Column(String(250), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postalCode = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(
        self,
        serviceType,
        laundryType,
        numberOfItems,
        phoneNumber,
        emailAddress,
        streetNumber,
        city,
        province,
        country,
        postalCode,
    ):
        """ Initializes a report service reading """
        self.serviceType = serviceType
        self.laundryType = laundryType
        self.numberOfItems = numberOfItems
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress
        self.streetNumber = streetNumber
        self.city = city
        self.province = province
        self.country = country
        self.postalCode = postalCode
        self.date_created = (
            datetime.datetime.now()
        )  # Sets the date/time record is created


    def to_dict(self):
        """ Dictionary Representation of a report service reading """
        dict = {}
        dict["id"] = self.id
        dict["serviceType"] = self.serviceType
        dict["laundryType"] = self.laundryType
        dict["streetAddress"] = {}
        dict["streetAddress"]["streetNumber"] = self.streetNumber
        dict["streetAddress"]["city"] = self.city
        dict["streetAddress"]["province"] = self.province
        dict["streetAddress"]["country"] = self.country
        dict["streetAddress"]["postalCode"] = self.postalCode
        dict["numberOfItems"] = self.numberOfItems
        dict["emailAddress"] = self.emailAddress
        dict["phoneNumber"] = self.phoneNumber
        dict["date_created"] = self.date_created

        return dict
