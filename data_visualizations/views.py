from django.shortcuts import render
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .utils import conversion as cv
from .utils import plotting as plt
import pandas as pd


from .models import Task

# Create your views here.

global_df = pd.DataFrame()
global_dtpes = None
global_id = 0
global_plot_id = 1


# Copy the file to the local server and save the path and label to the database.
# Pass to 'index' function to infer and convert the data and display the plot.
def upload(request):
    global global_df

    if request.method == "GET":
        return render(request, 'data_visualizations/upload.html')
    else:
        newtask = Task(label=request.POST['label'], file=request.FILES["file"])
        newtask.save()
        global_df = pd.DataFrame()

        return HttpResponseRedirect(reverse('index'))


# Changing the plot, pass it to 'index' function to render the plot.
def plot(request, id):
    global global_plot_id

    global_plot_id = id
    return HttpResponseRedirect(reverse('index'))


# Changing the dataset. Infer and convert the data, then pass it to index to display the plot.
def select(request, id):
    global global_df, global_dtpes, global_id

    task = Task.objects.get(pk=id)
    df = pd.read_csv(task.file)
    global_df, global_dtpes = cv.infer_and_convert_data_types(df)
    global_id = task.id

    return HttpResponseRedirect(reverse('index'))


# Infer and convert the data and render the plot.
def index(request, id=None):
    global global_df, global_dtpes, global_id, global_plot_id

    # if data never been inferred and converted.
    if len(global_df.index) == 0:

        # if no dataset is chosen, pick the last dataset that was uploaded.
        if id == None:
            task = Task.objects.all().order_by('uploaded_at').last()

            # if there is no dataset to be displayed, let the user upload new data
            if not task:
                return HttpResponseRedirect(reverse('upload'))

        else:
            task = Task.objects.get(pk=id)

        df = pd.read_csv(task.file)
        global_df, global_dtpes = cv.infer_and_convert_data_types(df)
        global_id = task.id

    alltasks = Task.objects.all()

    # Retrieve the plot imgae.
    plot = plt.get_plot(global_df, global_plot_id)

    return render(request, 'data_visualizations/index.html', {
        'plot': plot, # plot image
        'data_types': global_dtpes, # data types and probability for each column
        'alltasks': alltasks, # all uploaded dataset, allow user to change dataset
        'task': global_id, # active dataset
        'plot_id': global_plot_id, # active plot
        'dataframe': global_df # all data in the dataset, displayed on the table
    })
