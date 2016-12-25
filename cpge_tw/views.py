from django.shortcuts import render
from reco.forms import *
from django.contrib.contenttypes.models import ContentType
from reco.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def index(request, loginMsg=""):
    article_list = Article.objects.order_by('-date')[:3]
    for article in article_list:
        article.content = article.content[:6]
    context_dict = {
        'newArticles': article_list,
        'loginMsg' : loginMsg,
    }
    return render(request, 'cpge_tw/index.html', context_dict)

def article(request,articleID):
    returnForm = {}
    try:
        article = Article.objects.get(id=articleID)
        returnForm['title'] = article.title
        returnForm['content'] = article.contentHtml
    except Article.DoesNotExist:
        HttpResponseRedirect('/')
    return render(request, 'cpge_tw/article.html', returnForm)

def articlecomment(request, articleID):
    if request.method == 'POST':
        currentArticle = Article.objects.get(id=articleID)  
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            commentweb = comment_form.save(commit=False)
            comment = Comment(parent=currentArticle)
            comment.content = commentweb.content
            if commentweb.name:
                comment.name = commentweb.name
            if request.user.is_authenticated():
                comment.author=UserProfile.objects.get(user = request.user)
            comment.save()
            return HttpResponseRedirect('/article/'+articleID)

def replycomment(request, commentID, articleID):
    comment = Comment.objects.get(id=commentID)
    if request.method == 'GET':        
        commentType = ContentType.objects.get_for_model(comment)
        replys = Comment.objects.filter(content_type = commentType.id, object_id = commentID)
        return render(request, 'get-replys.html', {'replys': replys})
    elif request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            reply_ = reply_form.save(commit=False)
            reply = Comment(parent=comment)
            reply.content = reply_.content
            if reply_.name:
                reply.name = reply_.name
            if request.user.is_authenticated():
                reply.author=UserProfile.objects.get(user = request.user)
            reply.save()
        return HttpResponseRedirect('/article/'+articleID)

@login_required
def answer(request, questionID):
    question = Question.objects.get(id = questionID)
    print(question.id)
    if request.method == "POST":
        reply_form = AnswerForm(request.POST)
        if reply_form.is_valid():
            try:
                 answer = question.answer
                 print(answer.id)
                 answer_ = reply_form.save(commit=False)
                 answer.content = answer_.content
            except:
                answer = reply_form.save(commit=False)
            answer.author = UserProfile.objects.get(user = request.user)
            answer.question = question
            answer.save()
    return HttpResponseRedirect('/questionlist/')

def articlelist(request):
    articles = Article.objects.order_by('-date')    
    context_dict = {
        'articles' : articles 
    }
    return render(request, 'cpge_tw/article-list.html', context_dict)

def questionlist(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    context_dict = {
        'questions' : questions,
    }
    return render(request, 'cpge_tw/questionList.html', context_dict)

def addquestion(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save()
            question.save()
    return HttpResponseRedirect('/questionlist')

@login_required
def createarticle(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        current_user = UserProfile.objects.get(user = request.user)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = current_user
            article.save()
            return HttpResponseRedirect('/articlelist')
        else:
            print(article_form.errors)
    else:
        article_form = ArticleForm()
    return render(request, 'cpge_tw/create-article.html', {'form':article_form})

@login_required
def editarticle(request,articleID):
    currentArticle = Article.objects.get(id=articleID)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            articleEdited = article_form.save(commit=False)
            currentArticle.title = articleEdited.title
            currentArticle.content = articleEdited.content
            currentArticle.save()

            return article(request,articleID)
            print(article_form.errors)
    else:
        article_form = ArticleForm()
    return render(request, 'cpge_tw/create-article.html', {'article':currentArticle, 'form':article_form})

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.is_active = False
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'cpge_tw/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.POST:
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return index(request, "Wait for activation")
        else:
            return index(request, "Login Error")
            # Bad login details were provided. So we can't log the user in.

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # return render(request, 'cpge_tw/login.html', {})
        return index(request, "Login Error")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def contact(request):
    users = UserProfile.objects.filter(ispublic=True)
    return render(request, 'cpge_tw/contact.html', {'users':users} )

def test(request):
    return render(request, 'test.html')

def qAndA(request):
    f = open('static/html/qAndA.html','r')
    s = ''
    for line in f:
        s += line
    return render(request, 'cpge_tw/qAndA.html', {'questions':s})
