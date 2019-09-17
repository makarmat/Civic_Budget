from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect
from django.views import View

from django.contrib import messages
from projects.forms import AddOriginatorForm, AddProjectDetailForm, AddCostForm, CommentForm, LoginForm, VoteForm
from projects.models import Originator, Cost, Project, Voter


class AddOriginatorView(View):
    def get(self, request):
        form = AddOriginatorForm()
        return render(request, 'add_project.html', {'form': form})

    def post(self, request):
        form = AddOriginatorForm(request.POST)
        if form.is_valid():
            originator = form.save(commit=False)
            originator.save()
            request.session['originator_id'] = originator.id
            return redirect('add_project_details')
        return render(request, 'add_project.html', {'form': form})


class AddProjectDetailView(View):
    def get(self, request):
        originator_id = request.session.get('originator_id')
        if originator_id:
            originator = Originator.objects.get(pk=originator_id)
            form = AddProjectDetailForm(initial={
                'originator_id': originator_id
            })
            return render(request, 'add_project_detail.html', {
                'form': form,
                'originator': originator
            })
        return HttpResponseForbidden()

    def post(self, request):
        form = AddProjectDetailForm(request.POST)
        originator_id = request.session.get('originator_id')
        if request.POST['action'] == 'Dalej':
            if form.is_valid():
                if originator_id == form.cleaned_data['originator_id']:
                    project_details = form.save(commit=False)
                    originator = Originator.objects.get(pk=originator_id)
                    project_details.originator = originator
                    project_details.save()
                    print(project_details.id)
                    request.session['project_id'] = project_details.id
                    return redirect('add_project_costs')
                raise Http404
            return render(request, 'add_project_detail.html', {'form': form})

        if request.POST['action'] == 'back':
            if originator_id == int(request.POST['originator_id']):
                return redirect('edit_project')
            raise Http404


class AddCostView(View):
    def get(self, request):
        originator_id = request.session.get('originator_id')
        if originator_id:
            originator = Originator.objects.get(pk=originator_id)
            costs = Cost.objects.filter(originator=originator)
            total_cost = 0
            grant_total_cost = 0
            other_total_cost = 0
            t_list = (c.whole_cost for c in costs)
            g_list = (c.grant_cost for c in costs)
            o_list = (c.other_cost for c in costs)
            for n in t_list:
                total_cost += n

            for n in g_list:
                grant_total_cost += n

            for n in o_list:
                other_total_cost += n

            form = AddCostForm(initial={
                'originator_id': originator_id
            })
            args = {
                'form': form,
                'costs': costs,
                'originator': originator,
                'total_cost': total_cost,
                'grant_total_cost': grant_total_cost,
                'other_total_cost': other_total_cost
            }
            return render(request, 'add_project_cost.html', args)
        return HttpResponseForbidden()

    def post(self, request):
        if request.POST['action'] == 'add_cost':
            form = AddCostForm(request.POST)
            originator_id = request.session.get('originator_id')
            if form.is_valid():
                if originator_id == form.cleaned_data['originator_id']:
                    cost_name = form.cleaned_data['cost_name']
                    grant_cost = form.cleaned_data['grant_cost']
                    other_cost = form.cleaned_data['other_cost']
                    whole_cost = grant_cost + other_cost
                    originator = Originator.objects.get(pk=originator_id)
                    Cost.objects.create(cost_name=cost_name, grant_cost=grant_cost, other_cost=other_cost,
                                        whole_cost=whole_cost, originator=originator)
                    return redirect('add_project_costs')
                raise Http404
            return render(request, 'add_project_cost.html', {'form': form})

        if request.POST['action'] == 'del':
            originator_id = request.session['originator_id']
            if originator_id == int(request.POST['originator_id']):
                cost_id = request.POST['cost_id']
                cost = Cost.objects.get(pk=cost_id)
                cost.delete()
                return redirect('add_project_costs')
            raise Http404

        if request.POST['action'] == 'save_project':
            originator_id = request.session['originator_id']
            if originator_id == int(request.POST['originator_id']):
                return redirect('summary_view')
            raise Http404

        if request.POST['action'] == 'back':
            originator_id = request.session['originator_id']
            if originator_id == int(request.POST['originator_id']):
                return redirect('edit_project_details')
            raise Http404


def total_costs(costs):
    total_cost = 0
    grant_total_cost = 0
    other_total_cost = 0
    t_list = (c.whole_cost for c in costs)
    g_list = (c.grant_cost for c in costs)
    o_list = (c.other_cost for c in costs)
    for n in t_list:
        total_cost += n

    for n in g_list:
        grant_total_cost += n

    for n in o_list:
        other_total_cost += n

    all_costs = {
        'total_cost': total_cost,
        'grant_total_cost': grant_total_cost,
        'other_total_cost': other_total_cost
    }
    return all_costs


class SummaryView(View):
    def get(self, request):
        originator_id = request.session.get('originator_id')
        if originator_id:
            originator = Originator.objects.get(pk=originator_id)
            project = Project.objects.get(originator=originator)
            costs = Cost.objects.filter(originator=originator)
            total_cost = 0
            grant_total_cost = 0
            other_total_cost = 0
            t_list = (c.whole_cost for c in costs)
            g_list = (c.grant_cost for c in costs)
            o_list = (c.other_cost for c in costs)
            for n in t_list:
                total_cost += n

            for n in g_list:
                grant_total_cost += n

            for n in o_list:
                other_total_cost += n

            args = {
                'originator': originator,
                'project': project,
                'costs': costs,
                'total_cost': total_cost,
                'grant_total_cost': grant_total_cost,
                'other_total_cost': other_total_cost
            }
            return render(request, 'add_project_summary.html', args)
        return HttpResponseForbidden()

    def post(self, request):
        if request.POST['action'] == 'apply':
            originator_id = request.session.get('originator_id')
            if originator_id == int(request.POST['originator_id']):
                originator = Originator.objects.get(pk=originator_id)
                project = Project.objects.get(originator=originator)
                project.applied = True
                project.save()
                del request.session['originator_id']
                del request.session['project_id']
                return render(request, 'apply_confirm.html', {'project': project})
            raise Http404

        if request.POST['action'] == 'back':
            originator_id = request.session.get('originator_id')
            if originator_id == int(request.POST['originator_id']):
                return redirect('add_project_coasts')
            raise Http404


class EditOriginatorView(View):
    def get(self, request):
        originator_id = request.session['originator_id']
        if originator_id:
            originator = Originator.objects.get(pk=originator_id)
            form = AddOriginatorForm(instance=Originator.objects.get(pk=originator_id))
            return render(request, 'edit_project.html', {
                'form': form,
                'originator': originator
            })
        raise HttpResponseForbidden

    def post(self, request):
        originator_id = request.session.get('originator_id')
        originator = Originator.objects.get(pk=originator_id)
        form = AddOriginatorForm(request.POST, instance=originator)
        if form.is_valid():
            if originator_id == int(request.POST['originator_id']):
                form.save()
                project_id = request.session.get('project_id')
                if project_id:
                    return redirect('edit_project_details')
                return redirect('add_project_details')
            raise Http404
        return render(request, 'edit_project.html', {
            'form': form,
            'originator': originator
        })


class EditProjectDetailView(View):
    def get(self, request):
        originator_id = request.session.get('originator_id')
        originator = Originator.objects.get(pk=originator_id)
        if originator_id:
            project = Project.objects.get(originator=originator)
            form = AddProjectDetailForm(initial={
                'originator_id': originator_id
            }, instance=project)
            return render(request, 'edit_project_detail.html', {
                'form': form,
                'originator': originator
            })
        return HttpResponseForbidden()

    def post(self, request):
        originator_id = request.session.get('originator_id')
        originator = Originator.objects.get(pk=originator_id)
        project = Project.objects.get(originator=originator)
        form = AddProjectDetailForm(request.POST, instance=project)
        if request.POST['action'] == 'Dalej':
            if form.is_valid():
                if originator_id == form.cleaned_data['originator_id']:
                    form.save()
                    return redirect('add_project_costs')
                raise Http404
            return render(request, 'add_project_detail.html', {
                'form': form,
                'originator': originator
            })

        if request.POST['action'] == 'back':
            if originator_id == int(request.POST['originator_id']):
                return redirect('edit_project')
            raise Http404


class ProjectView(View):
    def get(self, request):
        projects = Project.objects.filter(applied=True)
        return render(request, 'projects.html', {'projects': projects})


class ProjectDetailView(View):
    def get(self, request, id):
        project = Project.objects.get(pk=id)
        originator = project.originator
        costs = Cost.objects.filter(originator=originator)
        form = CommentForm(initial={'comment': project.comment, 'verified': project.verified})
        all_costs = total_costs(costs)
        args = {
            'project': project,
            'originator': originator,
            'costs': costs,
            'form': form,
        }
        all_args = {**all_costs, **args}
        return render(request, 'project_detail.html', all_args)

    def post(self, request, id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            verified = form.cleaned_data['verified']
            project = Project.objects.get(pk=id)
            project.comment = comment
            project.verified = verified
            project.save()
            originator = project.originator
            costs = Cost.objects.filter(originator=originator)
            all_costs = total_costs(costs)
            args = {
                'project': project,
                'originator': originator,
                'costs': costs,
                'form': form,
            }
            all_args = {**all_costs, **args}
        return render(request, 'project_detail.html', all_args)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'projects'))
            else:
                messages.warning(request, 'Niepoprawny login i/lub hasło!')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class VoteView(View):
    def get(self, request):
        form = VoteForm()
        return render(request, 'vote.html', {'form': form})

    def post(self, request):
        voters = Voter.objects.all()
        pesel_list = [voter.pesel for voter in voters]
        phone_list = [voter.phone for voter in voters]
        form = VoteForm(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            phone = form.cleaned_data['phone']
            if pesel in pesel_list:
                messages.warning(request, 'Numer PESEL {} został już użyty do głosowania!'.format(pesel))
                return render(request, 'vote.html', {'form': form})
            if phone in phone_list:
                messages.warning(request, 'Numer telefonu został już użyty do głosowania!'.format(phone))
                return render(request, 'vote.html', {'form': form})
            form.save()
            sport_project = form.cleaned_data['sport_project']
            tourist_project = form.cleaned_data['tourist_project']
            cultural_project = form.cleaned_data['cultural_project']
            disabled_project = form.cleaned_data['disabled_project']
            civil_society_project = form.cleaned_data['civil_society_project']
            seniors_project = form.cleaned_data['seniors_project']
            craft_project = form.cleaned_data['craft_project']
            vote_list = []
            if sport_project:
                sport_project.votes += 1
                vote_list.append('{}. {}'.format(sport_project.id, sport_project.name))
                sport_project.save()
            if tourist_project:
                tourist_project.votes += 1
                vote_list.append('{}. {}'.format(tourist_project.id, tourist_project.name))
                tourist_project.save()
            if cultural_project:
                cultural_project.votes += 1
                vote_list.append('{}. {}'.format(cultural_project.id, cultural_project.name))
                cultural_project.save()
            if disabled_project:
                disabled_project.votes += 1
                vote_list.append('{}. {}'.format(disabled_project.id, disabled_project.name))
                disabled_project.save()
            if civil_society_project:
                civil_society_project.votes += 1
                vote_list.append('{}. {}'.format(civil_society_project.id, civil_society_project.name))
                civil_society_project.save()
            if seniors_project:
                seniors_project.votes += 1
                vote_list.append('{}. {}'.format(seniors_project.id, seniors_project.name))
                seniors_project.save()
            if craft_project:
                craft_project.votes += 1
                vote_list.append('{}. {}'.format(craft_project.id, craft_project.name))
                craft_project.save()
            print(vote_list)
            request.session['vote_list'] = vote_list
            return redirect('vote_confirm')
        return render(request, 'vote.html', {'form': form})


class VoteConfirmView(View):
    def get(self, request):
        vote_list = request.session.get('vote_list')
        if vote_list:
            del request.session['vote_list']
            return render(request, 'vote_confirm.html', {'vote_list': vote_list})
        return HttpResponseForbidden



