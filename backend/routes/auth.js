import express from 'express';
import passport from 'passport';

const router = express.Router();

router.get('/github', passport.authenticate('github', { scope: ['user:email', 'public_repo'] }));

router.get('/github/callback', 
  passport.authenticate('github', { failureRedirect: '/' }),
  (req, res) => {
    // Successfully authenticated, route back to frontend dashboard
    res.redirect(`http://localhost:5173/profile/${req.user.username}`);
  }
);

router.get('/logout', (req, res, next) => {
  req.logout((err) => {
    if (err) return next(err);
    res.status(200).json({ status: "logged_out" });
  });
});

export default router;
