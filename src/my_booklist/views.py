from django.views.generic import CreateView, DetailView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book
from .forms import BookForm

import requests
import numpy as np
from datetime import datetime


def isbn_checker(ISBN):
    if ISBN[:-1].isdecimal():
        if ISBN[-1] == 'X':
            chk_dig = 10
        else:
            chk_dig = int(ISBN[-1])

        isbn = np.array(list(map(int, ISBN)))

        if len(isbn) == 10:
            return (11 - sum(np.linspace(10, 2, 9) * isbn[:-1]) % 11) % 11 == chk_dig
        elif len(isbn) == 13:
            return (10 - sum(np.array([1, 3] * 6) * isbn[:-1]) % 10) % 10 == chk_dig
        else:
            return False
    else:
        return False


@login_required
def isbn_search(request):
    isbn = request.POST.get('isbn')
    redirect_url = '/?'

    if isbn_checker(isbn):
        url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(isbn)
        headers = {"content-type": "application/json"}
        req = requests.get(url, headers)
        data = req.json()

        query_list = ['isbn={}'.format(isbn)]

        if data['totalItems'] == 1:
            Info = data['items'][0]['volumeInfo']

            if 'title' in Info:
                query_list.append('title=' + Info['title'])

                if 'subtitle' in Info:
                    query_list.append('subtitle=' + Info['subtitle'])

            if 'authors' in Info:
                query_list.append('authors=' + '_'.join(Info['authors']))

            if len(query_list) > 1:
                redirect_url += '&'.join(query_list)
            else:
                redirect_url += 'error=true&{}'.format(query_list[0])
        else:
            redirect_url += 'error=true&{}'.format(query_list[0])
    else:
        redirect_url += 'error=true'

    return redirect(redirect_url)


class BookCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'

    model = Book
    form_class = BookForm
    template_name = "my_booklist/table.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all().order_by('category')
        context['username'] = self.request.user.username
        context['rent_count'] = Book.objects.filter(rent_user=self.request.user.username).count()
        return context

    def get_initial(self):
        initial = super(BookCreateView, self).get_initial()
        get_request = self.request.GET

        if not get_request.get('error'):
            if get_request.get('isbn'):
                initial['isbn'] = get_request.get('isbn')

            if get_request.get('title'):
                initial['title'] = get_request.get('title')

                if get_request.get('subtitle'):
                    initial['subtitle'] = get_request.get('subtitle')

            if get_request.get('authors'):
                authors_list = get_request.get('authors').split("_")
                authors_num = len(authors_list)

                if authors_num < 5:
                    for i in range(len(authors_list)):
                        initial['author{}'.format(i+1)] = authors_list[i]

                else:
                    for i in range(3):
                        initial['author{}'.format(i+1)] = authors_list[i]

                    initial['author4'] = ', '.join(authors_list[3:])
        else:
            initial['isbn'] = 'error'

        return initial

    def form_valid(self, form):
        messages.success(self.request, '書籍を追加しました')
        return super(BookCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '書籍を追加できませんでした')
        return super(BookCreateView, self).form_valid(form)


class DetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'

    model = Book
    template_name = 'my_booklist/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

@login_required
def RentNow(request, pk):
    book = Book.objects.get(pk=pk)

    if (not book.rent_flag) and book.rent_user is None:
        book.rent_flag = True
        book.rent_user = request.user.username
        book.rent_date = datetime.now()

        book.save()

    return redirect('detail', pk=pk)


class ReturnBooksView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'my_booklist/return_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        context['books'] = Book.objects.filter(rent_user=self.request.user.username)
        context['username'] = self.request.user.username

        return context


@login_required
def ReturnNow(request, pk):
    book = Book.objects.get(pk=pk)

    if book.rent_flag and book.rent_user == request.user.username:
        book.rent_flag = False
        book.rent_user = None
        book.rent_date = None
        book.save()

    return redirect(request.META['HTTP_REFERER'])
