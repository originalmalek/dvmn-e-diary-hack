import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Lesson, Commendation


def get_schoolkid(name):
    return Schoolkid.objects.get(full_name__contains=name)



def fix_marks(schoolkid):
    return schoolkid.mark_set.filter(points__lt=4).update(points=random.choice((4, 5)))


def remove_chastisements(schoolkid):
    return schoolkid.chastisement_set.all().delete()


def create_commendation(schoolkid, subject):
    commendations = (
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!'
    )
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date').first()

    return Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def main():
    try:
        kid = input('Введите полное имя ученика: ')
        schoolkid = get_schoolkid(kid)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        subject = input('Введите наименование предмета: ')
        create_commendation(schoolkid, subject)
    except ObjectDoesNotExist:
        print('Ученик не найден.')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников. Повторите действие.')


if __name__ == '__main__':
    main()