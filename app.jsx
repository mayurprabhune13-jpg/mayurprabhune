import React, { useEffect, useMemo, useState } from "react";
import { BrainCircuit, Rocket, Users, GraduationCap, Linkedin, Mail, Phone, ExternalLink, Star, Quote, Sparkles, ArrowLeft } from "lucide-react";
import { MobileNav } from "./mobile-nav";
import { useForm } from "./use-form";
import { showNotification } from "./notification";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

// ---------------------------------------------
// React + Tailwind + Framer Motion + Lucide + react-markdown
// Single-file site with a minimal hash router for a Blog index + Post pages
// Public figure site for Mayur Prabhune (AI Mentor)
// ---------------------------------------------

// ---- Simple hash router -----------------------------------------------------
function useHashRoute() {
  const [hash, setHash] = useState(window.location.hash || "#home");
  useEffect(() => {
    const onHash = () => setHash(window.location.hash || "#home");
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  return hash.replace(/^#\/?/, ""); // remove leading # or #/
}

// ---- Data -------------------------------------------------------------------
const nav = [
  { label: "Home", href: "#home" },
  { label: "About", href: "#about" },
  { label: "Services", href: "#services" },
  { label: "Testimonials", href: "#testimonials" },
  { label: "Blog", href: "#/blog" },
  { label: "Contact", href: "#contact" },
];

const services = [
  {
    title: "AI for Startups Bootcamp",
    desc: "A fast, practical deep-dive to turn AI into real traction in 1 day.",
    icon: <Rocket className="h-6 w-6" />,
    bullets: ["Founder-friendly toolkit", "Rapid small-wins", "Templates & prompts"],
  },
  {
    title: "AI + Leadership for Managers",
    desc: "Train managers to lead confidently in AI-first teams.",
    icon: <Users className="h-6 w-6" />,
    bullets: ["Decision frameworks", "Team upskilling", "Ethics & governance"],
  },
  {
    title: "AI Awareness for Students",
    desc: "Hands-on starter workshop for colleges & incubators.",
    icon: <GraduationCap className="h-6 w-6" />,
    bullets: ["Career pathways", "Tool demos", "Certificate included"],
  },
];

// CMS-ready markdown posts
// Replace this array by fetching from a headless CMS (Notion, Ghost, Strapi, etc.)
// or by dynamic import of /posts/*.md files.
const posts = [
  {
    slug: "tiny-ai-wins",
    title: "5 Tiny AI Wins Every Founder Can Ship This Week",
    date: "2025-08-20",
    summary: "Rapid, compounding wins beat big bang AI projects. Here are five you can deploy in hours, not months.",
    content: `# 5 Tiny AI Wins Every Founder Can Ship This Week\n\n**Why small beats big**: momentum > perfection.\n\n1. **Lead triage** – create a scoring prompt and tag hot leads.\n2. **Support macros** – draft-first replies, human finish.\n3. **Research briefs** – 1-page competitor or investor digests.\n4. **Meeting notes** – auto-summarize + action items.\n5. **Ops checklists** – turn SOPs into reusable prompt templates.\n\n> Ship one per week. In 30 days, your team will *feel* the lift.`,
  },
  {
    slug: "ai-leadership-playbook",
    title: "Leading in the Age of AI: A 3‑Step Playbook",
    date: "2025-08-22",
    summary: "Assess → Implement → Measure (A.I.M). A practical lens for managers to adopt AI with confidence.",
    content: `# Leading in the Age of AI: A 3‑Step Playbook\n\n**A.I.M** — Assess, Implement, Measure.\n\n- **Assess** readiness: skills, data, workflows.\n- **Implement** tiny pilots per team with owners.\n- **Measure** 90‑day KPIs: hours saved, quality gains, cycle time.\n\nRemember: AI augments people. Train *habits*, not just tools.`,
  },
  {
    slug: "prompt-systems",
    title: "Prompt Systems that Scale Beyond One Person",
    date: "2025-08-24",
    summary: "Turn ad‑hoc prompting into team systems with templates, guardrails, and examples.",
    content: `# Prompt Systems that Scale Beyond One Person\n\n1. **Templates** with inputs/outputs.\n2. **Examples** (few-shot) for consistency.\n3. **Guardrails** for tone, ethics, and data use.\n4. **Reviews** — weekly prompt retro.\n\nOutcome: repeatable quality across teams.`,
  },
];

const Stat = ({ value, label }) => (
  <div className="rounded-2xl border border-white/10 bg-white/5 px-6 py-4 text-center">
    <div className="text-3xl font-semibold tracking-tight">{value}</div>
    <div className="mt-1 text-sm text-white/70">{label}</div>
  </div>
);

// ---- Blog components ---------------------------------------------------------
function BlogIndex() {
  return (
    <section className="mx-auto max-w-5xl px-4 py-16">
      <div className="mb-6 flex items-center gap-3">
        <a href="#home" className="inline-flex items-center gap-2 text-white/70 hover:text-white"><ArrowLeft className="h-4 w-4"/> Home</a>
        <span className="text-white/40">/</span>
        <span className="text-white/80">Blog</span>
      </div>
      <h1 className="text-3xl font-semibold">Blog</h1>
      <p className="mt-2 text-white/80">Practical playbooks on AI adoption, leadership, and startup execution.</p>
      <div className="mt-8 grid md:grid-cols-2 gap-6">
        {posts.map((p) => (
          <article key={p.slug} className="rounded-2xl border border-white/10 bg-white/5 p-6 hover:bg-white/10 transition">
            <h2 className="text-xl font-medium">{p.title}</h2>
            <div className="mt-1 text-xs text-white/60">{new Date(p.date).toLocaleDateString()}</div>
            <p className="mt-3 text-sm text-white/80">{p.summary}</p>
            <a href={`#/blog/${p.slug}`} className="mt-4 inline-flex items-center gap-2 text-cyan-300 hover:underline">Read article <ExternalLink className="h-4 w-4"/></a>
          </article>
        ))}
      </div>
    </section>
  );
}

function BlogPost({ slug }) {
  const post = useMemo(() => posts.find((p) => p.slug === slug), [slug]);

  // Example: replace this with real CMS fetcher
  // async function loadFromCMS(slug) { const res = await fetch(`/api/posts/${slug}`); return await res.json(); }

  if (!post) {
    return (
      <section className="mx-auto max-w-5xl px-4 py-16">
        <a href="#/blog" className="inline-flex items-center gap-2 text-white/70 hover:text-white"><ArrowLeft className="h-4 w-4"/> Back to Blog</a>
        <h1 className="mt-6 text-2xl font-semibold">Post not found</h1>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-3xl px-4 py-16">
      <a href="#/blog" className="inline-flex items-center gap-2 text-white/70 hover:text-white"><ArrowLeft className="h-4 w-4"/> Back to Blog</a>
      <h1 className="mt-6 text-3xl font-semibold">{post.title}</h1>
      <div className="mt-1 text-xs text-white/60">{new Date(post.date).toLocaleDateString()}</div>
      <div className="prose prose-invert mt-6 max-w-none prose-a:text-cyan-300">
        <ReactMarkdown>{post.content}</ReactMarkdown>
      </div>
    </section>
  );
}

// ---- Main Site ---------------------------------------------------------------
export default function MayurAIMentorSite() {
  const route = useHashRoute();

  // Blog routes: "blog" index or "blog/:slug"
  if (route.startsWith("blog")) {
    const parts = route.split("/");
    const slug = parts[1];
    return slug ? (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white selection:bg-cyan-500/40">
        <SiteHeader />
        <BlogPost slug={slug} />
        <SiteFooter />
      </div>
    ) : (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white selection:bg-cyan-500/40">
        <SiteHeader />
        <BlogIndex />
        <SiteFooter />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white selection:bg-cyan-500/40">
      <SiteHeader />
      <Hero />
      <About />
      <Services />
      <Testimonials />
      <BlogPreview />
      <Contact />
      <SiteFooter />
    </div>
  );
}

// ---- Sections ----------------------------------------------------------------
function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur supports-[backdrop-filter]:bg-slate-950/50 border-b border-white/10">
      <div className="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
        <a href="#home" className="group inline-flex items-center gap-2">
          <div className="rounded-xl bg-cyan-500/20 p-2 ring-1 ring-cyan-500/30 group-hover:ring-cyan-300/60 transition">
            <BrainCircuit className="h-5 w-5 text-cyan-300" />
          </div>
          <span className="font-semibold tracking-tight">Mayur Prabhune</span>
          <span className="hidden sm:inline text-white/60">· AI Mentor</span>
        </a>
        <nav className="hidden md:flex items-center gap-6 text-sm">
          {nav.map((n) => (
            <a key={n.label} href={n.href} className="text-white/80 hover:text-white transition">
              {n.label}
            </a>
          ))}
          <a
            href="#contact"
            className="rounded-xl bg-cyan-500/20 px-4 py-2 text-cyan-300 ring-1 ring-cyan-500/40 hover:bg-cyan-500/30 transition"
          >
            Book a Workshop
          </a>
        </nav>
        <MobileNav nav={nav} />
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section id="home" className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(60rem_30rem_at_70%_-10%,rgba(34,211,238,0.15),transparent),radial-gradient(40rem_20rem_at_20%_-20%,rgba(147,51,234,0.12),transparent)]" />
      <div className="mx-auto max-w-7xl px-4 py-16 lg:py-24 grid lg:grid-cols-2 gap-10 items-center">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} viewport={{ once: true }}>
          <h1 className="text-4xl sm:text-5xl font-bold leading-tight tracking-tight">
            AI Mentor for <span className="text-cyan-300">Startups</span> &
            <br /> Future <span className="text-fuchsia-300">Leaders</span>
          </h1>
          <p className="mt-4 max-w-xl text-white/80">
            I help founders and managers turn AI into measurable outcomes—faster ops, sharper decisions, and teams who love using AI the right way.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <a href="#contact" className="rounded-xl bg-cyan-500 px-5 py-3 font-medium text-slate-950 hover:bg-cyan-400 transition">Book a Workshop</a>
            <a href="https://www.linkedin.com/in/mayur-prabhune" target="_blank" className="rounded-xl ring-1 ring-white/20 px-5 py-3 font-medium hover:bg-white/10 transition inline-flex items-center gap-2">
              <Linkedin className="h-4 w-4" /> Connect on LinkedIn
            </a>
          </div>
          <div className="mt-8 grid grid-cols-3 gap-3 max-w-lg">
            <Stat value="1200+" label="Learners Trained" />
            <Stat value="50+" label="Workshops & Talks" />
            <Stat value="12+" label="Years in L&D" />
          </div>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.98 }} whileInView={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, delay: 0.1 }} viewport={{ once: true }}>
          <div className="relative mx-auto w-full max-w-md">
            <div className="absolute -inset-1 rounded-[2rem] bg-gradient-to-tr from-cyan-500/30 via-fuchsia-500/20 to-transparent blur-2xl" />
            <div className="relative rounded-[2rem] border border-white/10 bg-white/5 p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-cyan-500/20 p-3 ring-1 ring-cyan-500/30">
                  <Sparkles className="h-5 w-5 text-cyan-300" />
                </div>
                <div>
                  <div className="text-sm text-white/60">Signature Framework</div>
                  <div className="font-semibold">A.I.M — Assess · Implement · Measure</div>
                </div>
              </div>
              <ul className="mt-4 space-y-2 text-sm text-white/80 list-disc pl-5">
                <li>Assess: quick AI readiness diagnostic for your team.</li>
                <li>Implement: hands-on playbooks for sales, ops, and L&D.</li>
                <li>Measure: 90‑day KPI dashboard to prove ROI.</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

function About() {
  return (
    <section id="about" className="mx-auto max-w-7xl px-4 py-16">
      <div className="grid lg:grid-cols-3 gap-8 items-start">
        <div className="lg:col-span-2">
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">About Mayur</h2>
          <p className="mt-3 text-white/80 max-w-3xl">
            Entrepreneur, trainer, and AI mentor on a mission to make AI practical for students, startups, and leaders. I combine
            real-world L&D experience with hands-on AI stacks so teams build momentum through small, compounding wins.
          </p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
          <div className="text-sm text-white/60">Focus Areas</div>
          <ul className="mt-2 grid gap-2 text-sm">
            <li>• AI adoption playbooks for founders</li>
            <li>• Manager enablement & prompt systems</li>
            <li>• Student pathways & portfolio projects</li>
          </ul>
        </div>
      </div>
    </section>
  );
}

function Services() {
  return (
    <section id="services" className="mx-auto max-w-7xl px-4 pb-8">
      <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">Services</h2>
      <div className="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((s) => (
          <motion.div
            key={s.title}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-5 hover:bg-white/10 transition"
          >
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-white/10 p-2">{s.icon}</div>
              <div className="font-medium">{s.title}</div>
            </div>
            <p className="mt-2 text-sm text-white/80">{s.desc}</p>
            <ul className="mt-3 space-y-1 text-sm text-white/70 list-disc pl-5">
              {s.bullets.map((b) => (
                <li key={b}>{b}</li>
              ))}
            </ul>
            <a href="#contact" className="mt-4 inline-flex items-center gap-2 text-cyan-300 hover:underline">
              Know more <ExternalLink className="h-4 w-4" />
            </a>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

function Testimonials() {
  const testimonials = [
    {
      name: "Sejal D.",
      role: "Startup Founder",
      quote:
        "Mayur's 90‑minute sprint gave us a working lead‑scoring prompt and saved ~6 hours/week. Immediate ROI.",
    },
    {
      name: "Rahul K.",
      role: "L&D Head, Retail",
      quote:
        "Clear frameworks + live demos. Our managers finally see where AI fits—and where it shouldn't.",
    },
    {
      name: "Ananya P.",
      role: "MBA Student",
      quote:
        "The student workshop was crisp and practical. I built my first AI portfolio project the same day!",
    },
  ];
  return (
    <section id="testimonials" className="mx-auto max-w-7xl px-4 py-16">
      <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">Testimonials</h2>
      <div className="mt-6 grid md:grid-cols-3 gap-6">
        {testimonials.map((t, i) => (
          <motion.figure
            key={i}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: i * 0.05 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-6"
          >
            <div className="flex items-center gap-2 text-cyan-300">
              <Quote className="h-4 w-4" />
              <Star className="h-4 w-4" />
              <Star className="h-4 w-4" />
              <Star className="h-4 w-4" />
              <Star className="h-4 w-4" />
            </div>
            <blockquote className="mt-3 text-white/90">{t.quote}</blockquote>
            <figcaption className="mt-4 text-sm text-white/70">
              {t.name} · {t.role}
            </figcaption>
          </motion.figure>
        ))}
      </div>
    </section>
  );
}

function BlogPreview() {
  return (
    <section id="blog" className="mx-auto max-w-7xl px-4 pb-16">
      <div className="flex items-end justify-between">
        <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">From the Blog</h2>
        <a href="#/blog" className="text-sm text-cyan-300 hover:underline">View all</a>
      </div>
      <div className="mt-6 grid md:grid-cols-3 gap-6">
        {posts.slice(0, 3).map((p) => (
          <article key={p.slug} className="rounded-2xl border border-white/10 bg-white/5 p-5 hover:bg-white/10 transition">
            <h3 className="font-medium">{p.title}</h3>
            <a href={`#/blog/${p.slug}`} className="mt-3 inline-flex items-center gap-2 text-cyan-300 hover:underline">
              Read article <ExternalLink className="h-4 w-4" />
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}

function Contact() {
  const { values, errors, isSubmitting, handleChange, handleSubmit } = useForm({
    name: "",
    email: "",
    message: "",
  });

  const onSubmit = async (formData) => {
    // Simulating API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    // In production, replace with actual API call
    console.log("Form submitted:", formData);
    showNotification("Thanks! We'll get back to you soon.", "success");
  };

  return (
    <section id="contact" className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(50rem_20rem_at_50%_-10%,rgba(34,211,238,0.15),transparent)]" />
      <div className="mx-auto max-w-7xl px-4 py-16">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-8 md:p-12 grid lg:grid-cols-3 gap-8 items-center">
          <div className="lg:col-span-2">
            <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight">Let's build your AI future</h2>
            <p className="mt-2 text-white/80 max-w-2xl">
              Book a free 20‑minute discovery call. We'll map your goals and pick the first three AI wins to ship this month.
            </p>
            <form onSubmit={(e) => { e.preventDefault(); handleSubmit(onSubmit); }} className="mt-6 grid sm:grid-cols-2 gap-3">
              <div className="relative">
                <input
                  name="name"
                  value={values.name}
                  onChange={handleChange}
                  className={`w-full rounded-xl bg-slate-950/60 px-4 py-3 ring-1 ${
                    errors.name ? "ring-red-500/50" : "ring-white/10"
                  } focus:ring-cyan-400 outline-none`}
                  placeholder="Your name"
                />
                {errors.name && <div className="absolute -bottom-5 left-0 text-xs text-red-500">{errors.name}</div>}
              </div>
              <div className="relative">
                <input
                  name="email"
                  value={values.email}
                  onChange={handleChange}
                  className={`w-full rounded-xl bg-slate-950/60 px-4 py-3 ring-1 ${
                    errors.email ? "ring-red-500/50" : "ring-white/10"
                  } focus:ring-cyan-400 outline-none`}
                  placeholder="Email address"
                />
                {errors.email && <div className="absolute -bottom-5 left-0 text-xs text-red-500">{errors.email}</div>}
              </div>
              <div className="relative sm:col-span-2">
                <textarea
                  name="message"
                  value={values.message}
                  onChange={handleChange}
                  rows={4}
                  className={`w-full rounded-xl bg-slate-950/60 px-4 py-3 ring-1 ${
                    errors.message ? "ring-red-500/50" : "ring-white/10"
                  } focus:ring-cyan-400 outline-none`}
                  placeholder="Tell me a bit about your goals…"
                />
                {errors.message && <div className="absolute -bottom-5 left-0 text-xs text-red-500">{errors.message}</div>}
              </div>
              <button
                type="submit"
                disabled={isSubmitting}
                className={`sm:col-span-2 rounded-xl ${
                  isSubmitting ? "bg-cyan-500/50" : "bg-cyan-500 hover:bg-cyan-400"
                } px-5 py-3 font-medium text-slate-950 transition relative`}
              >
                {isSubmitting ? "Sending..." : "Request call"}
              </button>
            </form>
          </div>
          <div className="space-y-3">
            <a href="mailto:mayur.prabhune@gmail.com" className="flex items-center gap-2 text-white/80 hover:text-white"><Mail className="h-4 w-4" /> mayur.prabhune@gmail.com</a>
            <a href="tel:+918799978054" className="flex items-center gap-2 text-white/80 hover:text-white"><Phone className="h-4 w-4" /> +91 87999 78054</a>
            <a href="https://www.linkedin.com/in/mayur-prabhune" target="_blank" className="flex items-center gap-2 text-white/80 hover:text-white"><Linkedin className="h-4 w-4" /> linkedin.com/in/mayur-prabhune</a>
          </div>
        </div>
      </div>
    </section>
  );
}

function SiteFooter() {
  return (
    <footer className="border-t border-white/10 py-8">
      <div className="mx-auto max-w-7xl px-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-sm text-white/60">
        <div>© {new Date().getFullYear()} Mayur Prabhune. All rights reserved.</div>
        <div className="flex items-center gap-4">
          <a href="#privacy" className="hover:text-white">Privacy</a>
          <a href="#terms" className="hover:text-white">Terms</a>
        </div>
      </div>
    </footer>
  );
}
