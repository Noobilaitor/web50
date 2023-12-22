from django import template

register = template.Library()

def skill(value):
    all_skills = value.split(",")
    return all_skills

register.filter("skill", skill)