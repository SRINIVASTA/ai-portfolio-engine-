import passport from 'passport';
import { Strategy as GitHubStrategy } from 'passport-github2';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
  const { data, error } = await supabase.from('users').select('*').eq('id', id).single();
  done(error, data);
});

passport.use(new GitHubStrategy({
    clientID: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET,
    callbackURL: process.env.GITHUB_CALLBACK_URL
  },
  async (accessToken, refreshToken, profile, done) => {
    const userData = {
      github_id: profile.id,
      username: profile.username,
      email: profile.emails?.[0]?.value || null,
      avatar_url: profile._json.avatar_url,
      oauth_token: accessToken
    };

    const { data, error } = await supabase
      .from('users')
      .upsert(userData, { onConflict: 'github_id' })
      .select()
      .single();

    return done(error, data);
  }
));

export default passport;
