===================================
Testting Django 1.7 Migrations
===================================

About this:
-----------------------------------

Just testing out the Django 1.7 Migrations!

Install:
--------

`pip install https://www.djangoproject.com/download/1.7c2/tarball/`

Workflow:
--------

### Creating the first migration
First lets go back in the code to when I just created the first migration for the polls app
by using the command `./manage.py makemigrations`:


    git checkout  d5eb2c5; find ./ -name "*.pyc" | xargs rm -v

**OBS**: The `find ./ -name "*.pyc" | xargs rm -v` part just removes the `.pyc`, and avoid some confusion in this workflow.

The next thing we need to do is execute our migrations, in this case it will:

* create the database and tables for django stuff
* migrate the polls/migrations/0001_initial, that is the first migration for the polls app

So lets run the command:

    ./manage.py migrate

After this we need to create our super user, to do this, we could just run the command:

    ./manage.py createsuperuser

Then run the server (`./manage.py runserver`) and look around a bit.

### Changing Choice.vote field to a Vote Model
Now let's try some schema migration. For this we'll replace the `vote` field in the `Choice` Model,
to a `Vote` model that have the user that made that vote.
So lets navigate to that commit:

    git checkout 10f5a53; find ./ -name "*.pyc" | xargs rm -v

You'll notice that we first created the `Vote` model then created the migration that represents it's creation.
For now we'll leave the `Choice.vote` field as it is.

Now, let's apply this migration:

    ./manage.py migrate

After this you run the server and see how things are.

You'll notice that now we have a Vote model, but we also have the Choice.vote field.
And that's not exacly what we wanted. So in the next step we'll remediate this.

### Migrating Choice.vote data to Vote Model
To simulate just a little on how it would be in a production scenario (when you can't simple just forget about the old data without migrating it), will do now a migration that will create a `Vote` model for each `Choice.vote`, and just to make things easier we'll consider the user as null (we could have a `ghost` user just like Github does in here).

To create a data migration you can run the command `./manage.py makemigrations --empty polls`, this will create a scheleton migration file that you can use to do your Data Migration.

So, let's checkout the code to see what I did for this Data Migration:

    git checkout 4e7112b; find ./ -name "*.pyc" | xargs rm -v

So let's first load some fixtures for our polls model:

    ./manage.py loaddata polls/fixtures/polls_0002.json

This have some objects for the models right after the last migration.

The file that does this migration is called `polls/migrations/0003_vote_field_to_model`.

If you take a close look you'll see that it has a method that does your data migration, and also a method that should be used if we needed to rollback this migration.

So now lets apply this migration:

    ./manage.py migrate

Run the server and you'll see now that we have a vote object that represents a vote for one of the Choices that were present in the fixtures.

### Reverting a migration
Now lets take a look at how we can control which migration we want to be in.
Lets revert this last Data Migration and go back to where we where.

To do this lets first checkout in what place we are:

    ./manage.py migrate -l polls

this should give us this:

    polls
     [X] 0001_initial
     [X] 0002_vote
     [X] 0003_vote_field_to_model


So lets go back to right after we created the vote model, that was in `0002_vote`:

    ./manage.py migrate polls 0002_vote

To confirm where we are, run againg the command `./manage.py migrate -l polls`, and check if it's like this:

    polls
     [X] 0001_initial
     [X] 0002_vote
     [ ] 0003_vote_field_to_model

Then run the server and you'll see that the `Vote` object is no more, and that the `Choice.vote` has the correct value that corresponded to the deleted `Vote` model

After this, you can re-apply the `0003_vote_field_to_model` migration:

    ./manage.py migrate polls 0003_vote_field_to_model

### Removing the Choice.vote field
Now that we are sure that our `Choice.vote` field data is migrated we can remove it.

To do this, we can just delete the model from models.py and then use the `./manage.py makemigrations` command.

So let's naviage to the code right after this was done:

    git checkout 5118080; find ./ -name "*.pyc" | xargs rm -v

Let's execute the migration.

Again, you can do this using `./manage.py migrate` or more specific `./manage.py migrate polls 0004_remove_choice_votes`.

After that you can run the server and check out that the `Choice.vote` field is gone.

LICENSE
=============
This software is distributed using MIT license, see LICENSE file for more details.
