import openai
import json
import time
import traceback
import csv
import ast
import pandas as pd
from functional import seq


class QuestionGenerator:

    def __init__(self, api_key):
        openai.api_key = api_key
        self.prompt = self.generate_prompt()

    def convert_keys_to_lowercase(self, dictionary):
        return {key.lower(): value for key, value in dictionary.items()}

    def get_completion(self, prompt, model="gpt-3.5-turbo", num_iterations=1):
        messages = [
            {"role": "system", "content": " you are a curriculum creator and teacher hiring expert who wanted to hire a subject expert and intelligent teacher. Design most difficult MCQ questions"},
            {"role": "user", "content": prompt},
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message["content"]

    def generate_prompt(self):
        prompt = """
        -You are creating a test to find best teacher who can teach for "Grade VI" or class VI CBSE and IG board in India
        - You must Create very hard or difficult “Multiple choice questions” on "Science subject" with 4 options and one correct answer, where “None 
        of the above” and “all of the above” should not be an option.

        - Provide them into valid JSON array of object for Multiple choice questions in below formats :
        
        \n[{\"question\": \"question Data \", \"option A\": \"option A Data values \" ,\"option B\": \"option B data values \",
        \"option C\": \"option C data values \", \"option D\": \"option D data values \", \"answer\": \" Option A or Option B or C or D \", 
        \"hint\": \"provide hint for answers \", \"feedback\": \"Feedback on correct answer \",\"bloom level\": understand, apply,analyze, etc.. \"Feedback on correct answer \", \"complexity\": \"complexity of question \",
        \"difficulty Level\": \"difficulty Level of question \", \"learning outcomes\": using Learning Outcomes\" }]\n  

        All questions must the below guidelines:
        
            1. Must Create most difficult questions only on given learning outcomes
            2. Tag each question to its learning outcome and knowledge points
            3. Give the correct answer along with the answer explanation
            4. Create questions based on apply, analysis, and understanding level of Bloom's taxonomy and must tag each question to the same.
            5. Must integrate multiple knowledge points and learning outcomes into a single problem use outcomes from  a given list to increase the complexity of the question for at least 60% of questions out of total questions
            6. Created questions should assess the Scientific knowledge of the attempting person.
            7. Create questions in the Indian context
            8. Include multiple distractors that reflect common mistakes, or misconceptions. Make sure that each option tests a different aspect of understanding, and all of them look plausible to increase the complexity.
            9. Must is Questions should be difficult and super difficult to complex level to solve for the teacher
            10. Questions should test teacher's analytical thinking, computational thinking, and logical thinking skills along with the knowledge so add such components in each question
            11. Be smart in asking questions and try not to repeat concepts in questions
            12. Divide and create three questions of  P1, P2 and P3 each where P1 means only one learning outcome, P2 means  > 1 and <=2 learning outcomes and Knowledge points clubbed together 
            and P3 means > 2 and <=3  learning outcomes  and knowledge points clubbed together.
            13. distribute the 9 questions evenly among understand, apply and analyze blooms level in P1, P2 and P3

        Learning Outcomes: 

            6CB.NT.1.1	identifies plant fibres on the basis of observable features i.e. appearance, texture, function, aroma, etc	Materials: Materials of daily use - Plant fibre, especially cotton and jute
            6CB.NT.1.2	identifies flowers on the basis of observable features i.e. appearance, texture, function, aroma, etc	The World of the Living: Plants - form and function - Structure of the flower; Morphological structure of the flower
            6CB.NT.2.1	differentiates fibre and yarn on the basis of their properties, structure and function	Material: Material of daily use - Different types of cloth material - cotton, wool, silk, synthetic
            6CB.NT.2.2	differentiates tap and fibrous root on the basis of their properties, structure and function	The World of the Living: Plants - form and function - Morphological structure and function of root
            6CB.NT.2.3	differentiates electrical conductors and insulators on the basis of their properties, structure and function	
            6CB.NT.3.1	classifies materials, organisms and processes based on observable properties e.g., materials as soluble and insoluble	
            6CB.NT.3.2	classifies materials, organisms and processes based on observable properties, e.g., materials as transparent, translucent and opaque	
            6CB.NT.3.3	classifies materials, organisms and processes based on observable properties, eg. changes as can be reversed and cannot be reversed	
            6CB.NT.3.4	classifies materials, organisms and processes based on observable properties, eg. plants as herbs, shrubs, trees, creeper, climbers	
            6CB.NT.3.5	classifies materials, organisms and processes based on observable properties, e.g. components of habitat as biotic and abiotic	
            6CB.NT.3.6	"classifies materials, organisms and processes based on observable properties, eg. motion as rectilinear, circular, periodic, etc."	
            6CB.NT.4.1	conducts simple investigations to seek answers to queries, e.g., What are the food nutrients present in animal fodder?	
            6CB.NT.4.2	conducts simple investigations to seek answers to queries, e.g., Can all physical changes be reversed?	
            6CB.NT.4.3	conducts simple investigations to seek answers to queries, e.g. Does a freely suspended magnet align in a particular direction?	
            6CB.NT.5.1	relates processes and phenomenon with causes, e.g., deficiency diseases with diet	
            6CB.NT.5.2	relates processes and phenomenon with causes, e.g., adaptations of animals and plants with their habitats	
            6CB.NT.5.3	relates processes and phenomenon with causes e.g., quality of air with pollutants	
            6CB.NT.6.1	explains processes and phenomenon, e.g., processing of plant fibres	
            6CB.NT.6.2	explains processes and phenomenon, e.g., movements in plants and animals	
            6CB.NT.6.3	explains processes and phenomenon, e.g., formation of shadows	
            6CB.NT.6.4	explains processes and phenomenon, e.g., reflection of light from plane mirror	
            6CB.NT.6.5	explains processes and phenomenon, e.g., variations in composition of air	
            6CB.NT.6.6	explains processes and phenomenon, e.g., preparatipn of vermicompost	
            6CB.NT.7	measures physical quantities and expresses in SI units, e.g., length	
            6CB.NT.8.1	draws labelled diagrams / flow charts of organisms and processes, e.g., parts of flowers	
            6CB.NT.8.2	draws labelled diagrams / flow charts of organisms and processes, e.g., joints	
            6CB.NT.8.3	draws labelled diagrams / flow charts of organisms and processes, e.g., filtration	
            6CB.NT.8.4	draws labelled diagrams / flow charts of organisms and processes, e.g., water cycle	
            6CB.NT.9.1	"constructs models using materials from surroundings and explains their working, e.g., pinhole camera"	
            6CB.NT.9.2	"constructs models using materials from surroundings and explains their working, e.g., periscope"	
            6CB.NT.9.3	"constructs models using materials from surroundings and explains their working, e.g., electric torch"	
            6CB.NT.10.1	 applies learning of scientific concepts in day-to-day life,e.g., selecting food items for a balanced diet	
            6CB.NT.10.2	"applies learning of scientific concepts in day-to-day life,e.g. separating materials"	
            6CB.NT.10.3	"applies learning of scientific concepts in day-to-day life,e.g selecting season appropriate fabrics"	
            6CB.NT.10.4	"applies learning of scientific concepts in day-to-day life,e.g using compass needle for finding directions"	
            6CB.NT.10.5	"applies learning of scientific concepts in day-to-day life,e.g.suggesting ways to cope with heavy rain/drought"	
            6CB.NT.11.1	makes efforts to protect the environment, e.g., minimising wastage of food, water, electricity and generation of waste	
            6CB.NT.11.2	makes efforts to protect environment, e.g., spreading awareness to adopt rain water harvesting	
            6CB.NT.11.3	makes efforts to protect environment, e.g., care for plants	
            6CB.NT.12	exhibits creativity in designing, planning, making use of available resources, etc.	
            6CB.NT.13	"exhibits values of honesty, objectivity,cooperation, freedom from fear andprejudices"	
            6CB.NF.1.1	"recognise plant parts and animal products as sources of food; Cite examples; Identify what other animals eat"	
            6CB.NF.1.2	outline the components of food; state the sources and significance of each component for human health 	
            6CB.NF.2.1	identify the types of soil required for the growth of different fibrous plants	
            6CB.NF.2.2	discuss about saturated solutions	
            6CB.NF.2.3	infer that amount of substance dissolving varies with temperature	
            6CB.NF.2.4	infer that at the same temperature amounts of different substances that dissolves varies	
            6CB.NF.3.1	diferentiate between living and non-living things	
            6CB.NF.3.2	describe the effect of habitat in modifications in plants	
            6CB.NF.3.3	describe the structure and function of various parts of plants	
            6CB.NF.3.4	describe the Human skeletal system; state the function of the skeletal system;  identify different modes of movement in animals	
            6CB.NF.4	describe electric circuit	
            6CB.NF.5.1	define magnet; classy of objects into magnetic/non-magnetic objects;	
            6CB.NF.5.2	locate poles of a magnet	
            6CB.NF.5.3	discuss the properties of a magnet  

        The JSON object:

        """  
        return prompt
        

    def create_questions(self, repeat):
        output = []
        for i in range(repeat):
            try:
                response = self.get_completion(self.prompt)
                print('Pass ', i + 1)
                print(response)
                response_dict = json.loads(response)
                print('Type ', type(response_dict))

                if isinstance(response_dict, dict):
                    res = response_dict.values()
                    output.extend(res)
                else:
                    output.extend(response_dict)
            except Exception as e:
                print('Exception')
        return output

    def create_csv(self, output):
        updated_res = seq(output).map(lambda each : self.convert_keys_to_lowercase(each)).to_list()
        headers = list(updated_res[0].keys())
        questions_dir = set()
        filename = self.generate_filename()

        with open(filename, 'w', newline='') as f:
            try:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
            except Exception as e:
                print('Exception while writing csv')
                traceback.print_exc()

            for row in updated_res:
                question = row.get('questions') if row.get('questions') else row.get('question')
                if question:
                    question = question.lower()
                if question in questions_dir:
                    continue
                try:
                    writer.writerow(row)
                except Exception as e:
                    print('Exception while writing a row')
                    print(row)
                    traceback.print_exc()
                questions_dir.add(question)

        print(filename, ' created')
        return filename

    def generate_filename(self):
        filename = r'F:\Company_Data\Script_python\output_csv\questions.csv'
        return filename


if __name__ == '__main__':
    api_key = ""
    generator = QuestionGenerator(api_key)
    questions_data = generator.create_questions(repeat=1)
    filename = generator.create_csv(questions_data)
