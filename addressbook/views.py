from django.shortcuts import get_object_or_404, render_to_response
from models import Contact

def main(request):
    contacts = Contact.objects.all()
    recent_contacts = contacts.order_by('-date_created')[:10]
    return render_to_response('addressbook/main.html', locals())
    

def contact_detail(request, contact_id):
    #if request.is_ajax():
    contact = get_object_or_404(Contact, pk=contact_id)
    return render_to_response('addressbook/contact_detail.html', locals())
    #else:
    #    raise Exception('Non ajax request')