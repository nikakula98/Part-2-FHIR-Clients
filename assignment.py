from fhirclient import client
from fhirclient.models import patient, observation, humanname, identifier, fhirdate
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models import contactpoint as cp
from fhirclient.models import address as addr
from fhirclient.models.fhirabstractresource import FHIRAbstractResource
import traceback


class FHIRServer:

    def __init__(self):
        settings = {
            'app_id': '',
            'api_base': 'http://fhirserver.hl7fundamentals.org/fhir'
        }
        self.client = client.FHIRClient(settings=settings)

    def run(self):
        print(f'Is the client ready to make calls? {self.client.prepare()}')
        print(f'Is the server ready to accept calls? {self.client.server.ready}')

    def query_patient_data(self, resource_id: str, resource: FHIRAbstractResource):
        """
        Gets the resource information from resource in FHIR server using resource_id and parses through to get relevant information.

        Args:
            resource_id (str): The id of the resource.
            resource (FHIRAbstractResource): resource model of interest from the FHIR client

        Returns:
            custom result (dict): {Measurement name: measurement value}
        """
        custom_result = {}
        try:
            resource_data = resource.read(rem_id= resource_id,
                                             server = self.client.server)
            resource_response = resource_data.as_json()
            custom_result = {
                resource_response.get('code', {}).get('text'): resource_response.get('valueQuantity', {}).get('value')
            }
        except Exception as e:
            print(f'Error: {e} \n {traceback.format_exc()}')
        return custom_result

    def create_patient(self):
        """
        Function allows user to add in patient information into FHIR server using SMART library.

        Args:

        Returns:
            custom result (dict): {Patient category: Patient information}
        """
        new_patient = patient.Patient()
        new_patient.active = True
        new_patient.name = [humanname.HumanName({
            'family': 'Payton',
            'given': ['Walter']
        })]
        new_patient.identifier = [identifier.Identifier({
            'system': 'http://newpatient/mrn',
            'value': '123456789'
        })]
        new_patient.gender = 'male'
        new_patient.birthDate = fhirdate.FHIRDate('1962-01-01')
        response = new_patient.create(server=self.client.server)
        print(response)

    def update_patient(self, patient_id):
        """
        Function allows user to update patient information that is already existing in FHIR server using SMART library.

        Args:
            patient_id (str): The id of the patient as listed in the FHIR server.

        Returns:
            custom result (dict): {Patient category: Patient information}
        """
        # Step 1: load the existing patient resource from the server
        update_patient = patient.Patient.read(rem_id=patient_id,
                                              server=self.client.server)

        # Step 2: Modify the patient resource instance
        address = addr.Address()
        address.line = ['2300 Bashful Drive']
        address.city = 'Chicago'
        address.state = 'Illinois'
        address.postalCode = '60564'
        address.country = 'United States of America'
        update_patient.address = [address]

        phone = cp.ContactPoint()
        phone.system = 'phone'
        phone.value = '630-505-9825'
        update_patient.telecom = [phone]
        response = update_patient.update(server=self.client.server)
        print(response)



    def delete_patient(self, patient_id):
        """
        Function allows user to delete patient information that is in FHIR server using SMART library.

        Args:
            patient_id (str): The id of the patient as listed in the FHIR server.

        Returns:

        """
        delete_patient = patient.Patient.read(rem_id=patient_id,
                                              server=self.client.server)
        response = delete_patient.delete(server=self.client.server)
        print(response)

fs = FHIRServer()
result = fs.query_patient_data('14', resource = observation.Observation)
print(result)

fs.create_patient()
fs.update_patient(patient_id='142303')
fs.delete_patient(patient_id='142303')

