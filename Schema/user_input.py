# Pydantic model :- 


from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal

from config.city_tier import tier_1_cities, tier_2_cities


class UserInput(BaseModel):

    age: int = Field(...,gt=0,le=120,description="Age of the user")
    weight: float = Field(...,gt=0,description="Weight of the user in kg")
    height: float = Field(...,gt=0,description="Height of the user in cm")
    income_lpa: float = Field(...,gt=0,description="Income of the user in lakhs per annum")
    smoker: Literal['yes', 'no'] = Field(...,description="Smoking status of the user")
    city: str = Field(...,description="City of the user")
    occupation:Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'] = Field(...,description="Occupation of the user")
    


    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v 


# 1st Computed Field

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height / 100)**2
        
# 2nd Computed Field
        
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker == 'yes' and self.bmi > 30:
            return "high"
        elif self.smoker == 'yes' or self.bmi > 27:
            return "medium"
        else:
            return "low" 
    
        
# 3rd Computed Field

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"   
        

# 4th Computed Field

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3