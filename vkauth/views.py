from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import requests
import json


class LoginView(View):
    def get(self, request):
        return render(request, 'vkauth/index.html')


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        social_user = request.user.social_auth.filter(provider='vk-oauth2').first()
        context = {}
        if social_user:
            friends = requests.get('https://api.vk.com/method/friends.get',
                                   params=dict(user_ids=social_user.uid,
                                               fields="photo_100,domain",
                                               order='random',
                                               access_token=social_user.extra_data['access_token'],
                                               count=5,
                                               v="5.120"))
            context['friends'] = friends.json()['response']['items']

            vk_user = requests.get('https://api.vk.com/method/users.get',
                                   params=dict(user_ids=social_user.uid,
                                               fields="photo_200,domain,online",
                                               access_token=social_user.extra_data['access_token'],
                                               v="5.120"))
            context['vk_user'] = vk_user.json()['response'][0]

        return render(request, 'vkauth/friends.html', context=context)
