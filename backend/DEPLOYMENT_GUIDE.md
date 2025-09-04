# Deployment Guide: Django on Vercel with Supabase

This guide will walk you through deploying your Django application to Vercel with a Supabase database.

## Prerequisites

1. **Git** - [Download Git](https://git-scm.com/download/win)
2. **Node.js** (for Vercel CLI) - [Download Node.js](https://nodejs.org/)
3. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
4. **Vercel Account** - [Sign up here](https://vercel.com/signup)
5. **Supabase Project** - [Create one here](https://supabase.com/)

## Step 1: Set Up Environment Variables

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
2. Edit `.env` and fill in all the required values.
3. **Important**: Add `.env` to your `.gitignore` file to prevent committing sensitive data.

## Step 2: Install Dependencies

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

## Step 3: Set Up Git

1. Initialize a Git repository (if not already done):
   ```bash
   git init
   ```
2. Add all files and make an initial commit:
   ```bash
   git add .
   git commit -m "Initial commit"
   ```
3. Create a new repository on GitHub and push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo.git
   git branch -M main
   git push -u origin main
   ```

## Step 4: Deploy to Vercel

1. Log in to Vercel:
   ```bash
   vercel login
   ```
2. Deploy your application:
   ```bash
   vercel
   ```
   - Follow the prompts to link your project
   - Choose to deploy to a new project
   - Use default settings for most options

## Step 5: Configure Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add all variables from your `.env` file
5. Mark sensitive variables as "Secret"

## Step 6: Set Up Supabase

1. In your Supabase dashboard, go to Project Settings > Database
2. Note your database connection details
3. Update your `.env` file with these details
4. In Vercel, update the environment variables with these details

## Step 7: Run Database Migrations

1. Connect to your Vercel project via SSH:
   ```bash
   vercel ssh
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Step 8: Deploy to Production

1. Deploy to production:
   ```bash
   vercel --prod
   ```
2. Your application will be available at: `https://your-project.vercel.app`

## Troubleshooting

- **Database Connection Issues**: Verify your Supabase connection string and network settings
- **Environment Variables**: Ensure all required variables are set in Vercel
- **Static Files**: If you have static files, configure `STATICFILES_DIRS` in `settings.py`
- **Logs**: Check Vercel logs for errors: `vercel logs`

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Django on Vercel](https://vercel.com/guides/deploying-django-with-vercel)
- [Supabase Documentation](https://supabase.com/docs)

## Support

If you encounter any issues, please refer to the documentation or open an issue in the repository.
