from django.shortcuts import render
from reco.forms import *
from django.contrib.contenttypes.models import ContentType
from reco.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from reco.functions import latexToHtml
import subprocess

def index(request, loginMsg=""):
    articles = Article.objects.order_by('-date')[:3]
    newArticles = []
    for a in articles:
        tmp = {}
        tmp['title'] = a.title
        tmp['abstract'] = a.abstract
        tmp['id'] = a.id 
        newArticles.append(tmp)
    context_dict = {
        'newArticles': newArticles,
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
def editArticle(request,articleID):
    returnForm = {}
    currentArticle = Article.objects.get(id=articleID)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        data = request.POST
        if article_form.is_valid():
            currentArticle.title = data['title']
            currentArticle.contentLtx = data['contentLtx']
            currentArticle.abstract = data['abstract']
            currentArticle.save()
            return HttpResponseRedirect(reverse('article', args=(str(currentArticle.id),)))
    else:
        returnForm['currentArticle'] = currentArticle
    return render(request, 'admin/newArticle.html', returnForm)

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
    f = open('static/html/q_and_a.html','r')
    s = ''
    for line in f:
        s += line
    f.close()
    return render(request, 'cpge_tw/qAndA.html', {'questions':s})

@login_required
def newArticle(request):
    returnForm = {}
    # Gallery is a imgform set
    if request.method == 'POST':
        data = request.POST
        form = ArticleForm(request.POST)
        if form.is_valid():
            print(form)
            currentArticle = form.save()
            return HttpResponseRedirect(reverse('article', args=(str(currentArticle.id),)))
    articleForm = ArticleForm()
    # Get no version details by get request
    returnForm['form'] = articleForm
    return render(request, 'admin/newArticle.html',returnForm)

@login_required
def pageEdit(request,page):
    allowLst = ['q_and_a']
    if page in allowLst:
        if request.method == 'POST':
            contentLtx = request.POST['contentLtx']
            latexToHtml(contentLtx)
            subprocess.call('cp tmp/tmp.tex static/tex/'+page+'.tex',shell=True) 
            subprocess.call('cp tmp/tmpS.html static/html/'+page+'.html',shell=True)
            subprocess.call('rm tmp/*.*', shell=True)
            return HttpResponseRedirect('/'+page)
        f = open('static/tex/'+page+'.tex','r')
        s = ''
        for line in f:
            s += line
        f.close()
        returnForm = {}
        returnForm['page'] = page
        returnForm['contentLtx'] = s
        return render(request, 'admin/pageEdit.html',returnForm)
    else:
        return HttpResponseRedirect('/')

@login_required
def userSettings(request,errMsg="", msg=""):
    returnForm = {}
    setMsg(returnForm)
    if request.method =='POST':
        data = request.POST
        request.method=""
        if not request.user.check_password(data['OldPassword']):
            errMsg="密碼錯誤"
            return userSettings(request,errMsg=errMsg)
        else:
            if data['InputPassword1'] != "":
                if data['InputPassword1'] != data['InputPassword2']:
                    errMsg = "驗證密碼不符"
                    return userSettings(request,errMsg=errMsg, msg=msg)
                else:
                    user = request.user
                    user.set_password(data['InputPassword1'])
                    user.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    msg += '密碼已更新'
    returnForm['errMsg'] = errMsg
    returnForm['msg'] = msg
    return render(request, 'admin/settings.html', returnForm)

def setMsg(returnForm):
    returnForm['msg'] = ''
    returnForm['errMsg'] = ''
    returnForm['warnMsg'] = ''
    return returnForm

def download(request):
    annalsYears = []
    for i in range(2004,2018):
        annalsYears.append(str(i))
    annalsYears.insert(3,'2006-1')
    returnForm = {}
    returnForm['annalsYears'] = annalsYears
    return render(request, 'cpge_tw/download.html', returnForm)
