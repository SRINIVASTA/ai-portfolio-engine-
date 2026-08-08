import express from 'express';
import session from 'express-session';
import cors from 'cors';
import passport from './config/passport.js';
import authRoutes from './routes/auth.js';
import syncRoutes from './routes/sync.js';
import chatRoutes from './api/chat.js';

const app = express();

app.use(cors({ origin: 'http://localhost:5173', credentials: true }));
app.use(express.json());
app.use(session({ secret: 'saas_portfolio_secret', resave: false, saveUninitialized: false }));

app.use(passport.initialize());
app.use(passport.session());

// Mount multi-tenant operational API points
app.use('/auth', authRoutes);
app.use('/api', syncRoutes);
app.use('/api', chatRoutes);

const PORT = 3000;
app.listen(PORT, () => console.log(`SaaS Platform Server actively listening on port ${PORT}`));
