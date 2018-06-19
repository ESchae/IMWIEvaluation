from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from base import Base


participation = Table(
    'participation', Base.metadata,
    Column('lecture_id', Integer, ForeignKey('lecture.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)


class Lecture(Base):
    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    tutorial = Column(Boolean)
    lecturer_id = Column(Integer, ForeignKey('lecturer.id'))
    semester_id = Column(Integer, ForeignKey('semester.id'))

    semester = relationship("Semester", back_populates="lectures")

    # many to one relationship between lectures and lecture
    # compare with declaration in lecture.py
    lecturer = relationship("Lecturer", back_populates="lectures")

    # many to many relationship between lecture and student
    # expressed in association table participation (see above)
    participants = relationship("Student", secondary=participation,
                                backref="lectures")

    def __init__(self, title, tutorial, lecturer):
        self.title = title
        self.tutorial = tutorial
        self.lecturer = lecturer
