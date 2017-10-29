from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

# A small helper function to work out the interest value

def calc_interest(value):
    if value <= 0:
        interest_rate = 0
    else:
        if value <= 1000:
            interest_rate = 1
        else:
            if value > 1000:
                interest_rate = 2
            if value > 5000:
                interest_rate = 3
    return interest_rate


# Create your views here.

def ee_index_view(request):
    context = {}
    MAX_DEPOSIT = getattr(settings, "EE_MAX_VALUE", 10000000)
    context['max_value']=MAX_DEPOSIT

    return render(request, 'eetest-landing-page.html', context)


def ee_calculated_interest(request):
    print("***** Calculated interest view hit *****")
    context = {}
    if 'ee_calculate' in request.POST:
        deposit_string=request.POST['ee_calculate']
        print("*** got value in ee calculate of: {} ***".format(deposit_string))

        try:
            deposit_number=float(deposit_string)

            MAX_DEPOSIT = getattr(settings, "EE_MAX_VALUE", 10000000)
            if deposit_number>MAX_DEPOSIT:
                context['error'] = "You can only deposit a maximum of £ {}".format(MAX_DEPOSIT)
                return render(request, 'eetest-landing-page.html', context)

        except ValueError:
            print ("This string contains non digits")
            context['error']="Please only type a number between 0 and 10,000,000 and then press the calculate button"
            return  render(request, 'eetest-landing-page.html', context)

        interest_rate = calc_interest(deposit_number)
        interest = deposit_number *(float(interest_rate)/100)
        total = deposit_number+interest

        # Populate context values
        context['deposit']= str(deposit_number)
        context['interest']= str(interest)
        context['interest_rate']= str(interest_rate)
        context['total']= str(total)

        print("*** Context is now: {}".format(context))



    return render(request, 'eetest-interest-rate.html', context)
