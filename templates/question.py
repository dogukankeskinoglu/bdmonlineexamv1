#Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puanı)
class Question:

    def __init__(self,q_exam_id,q_content,q_choices,correct_answer,q_point): 
        #self.question_id=q_id
        self.question_exam_id=q_exam_id
        self.question_content=q_content
        self.question_choices=q_choices
        self.correct_answer=correct_answer
        self.question_point=q_point
    
    def __init__(self):
        pass


    