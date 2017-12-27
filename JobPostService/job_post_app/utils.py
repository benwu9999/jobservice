import operator

from django.db.models import Q

from models import JobPost


def get_employer_ids(employer_names, employers_by_name_dict):
    r = []
    for n in employer_names:
        r.extend(employers_by_name_dict[n])
    return r


def get_location_ids(location_names, location_by_name_dict):
    r = []
    for n in location_names:
        r.extend(location_by_name_dict[n])
    return r


def generate_match(query, employers_by_text_dict, location_by_text_dict):
    qs = list()

    terms = query.terms
    if not terms:
        query_set = JobPost.objects.all();
    else:
        full_text_search_terms = ' +'.join(terms)
        query_set = JobPost.full_text_search_objects.search(full_text_search_terms)

    employer_names = query.employer_names
    if employer_names:
        # custom lookup
        employer_ids = get_employer_ids(employer_names, employers_by_text_dict)
        # https: // dev.mysql.com / doc / refman / 5.5 / en / fulltext - boolean.html
        qs.append(Q(**{'employer_profile_id__in': employer_ids}))
        # i.e. MATCH (employer_profile_id) AGAINST (e1 e2 e3 IN BOOLEAN MODE)
        # match either e1 e2 OR e3

    location_names = query.locations
    if location_names:
        # custom lookup
        location_ids = get_location_ids(location_names, location_by_text_dict)
        qs.append(Q(**{'location_id__in': location_ids}))
        # d['title,description__search'] = ' +'.join(terms)
        # full text search of keywords,
        # i.e. MATCH (title,description) AGAINST (k1 +k2 +3 IN BOOLEAN MODE)
        # match k1 k2 AND k3

    if query.last_updated:
        qs.append(Q(**{'modified__gte': query.last_updated_w_tz()}))

    # if query.compensation and query.compensation_unit:
    #     d['compensation_amount__range'] = (query.compensation[0], query.compensation[1])
    #     d['compensation_duration'] = query.compensation_unit
    # if query.updated:
    #     d['modified__gt'] = query.updated
    # if query.has_contact != None:
    #     d['has_contact'] = query.has_contact
    if qs:
        matched_job_posts = query_set.filter(reduce(operator.and_, qs))
    else:
        matched_job_posts = query_set
    return matched_job_posts
