// Navigation Items
const navItems = [
  { label: "Home", href: "#home" },
  { label: "Services", href: "#services" },
  { label: "About", href: "#about" },
  { label: "Testimonials", href: "#testimonials" },
  { label: "Contact", href: "#contact" }
];

// Header Component
const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-[#111818]/80 backdrop-blur">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="text-[var(--primary-cyan)]">
              <svg className="h-8 w-8" fill="none" viewBox="0 0 48 48">
                <path fill="currentColor" d="M42.1739 20.1739L27.8261 5.82609C29.1366 7.13663 28.3989 10.1876 26.2002 13.7654C24.8538 15.9564 22.9595 18.3449 20.6522 20.6522C18.3449 22.9595 15.9564 24.8538 13.7654 26.2002C10.1876 28.3989 7.13663 29.1366 5.82609 27.8261L20.1739 42.1739C21.4845 43.4845 24.5355 42.7467 28.1133 40.548C30.3042 39.2016 32.6927 37.3073 35 35C37.3073 32.6927 39.2016 30.3042 40.548 28.1133C42.7467 24.5355 43.4845 21.4845 42.1739 20.1739Z"/>
              </svg>
            </div>
            <div className="font-bold tracking-tight">Mayur Prabhune</div>
          </div>

          <nav className="hidden md:flex items-center gap-8">
            {navItems.map(item => (
              <a key={item.href} href={item.href} className="text-sm text-white/70 hover:text-white transition-colors">
                {item.label}
              </a>
            ))}
            <button className="rounded-lg bg-[var(--primary-cyan)] px-4 py-2 text-sm font-semibold text-black hover:opacity-90 transition-opacity">
              Book a Call
            </button>
          </nav>

          <button 
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-white/10">
          <nav className="flex flex-col p-4 gap-4">
            {navItems.map(item => (
              <a key={item.href} href={item.href} className="text-white/70 hover:text-white transition-colors">
                {item.label}
              </a>
            ))}
            <button className="rounded-lg bg-[var(--primary-cyan)] px-4 py-2 text-sm font-semibold text-black hover:opacity-90 transition-opacity">
              Book a Call
            </button>
          </nav>
        </div>
      )}
    </header>
  );
};

// Hero Section
const Hero = () => (
  <section id="home" className="relative overflow-hidden">
    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(60rem_30rem_at_70%_-10%,rgba(6,249,249,0.15),transparent),radial-gradient(40rem_20rem_at_20%_-20%,rgba(249,6,249,0.12),transparent)]"/>
    <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
            AI Mentor for <span className="gradient-text">Startups</span> &<br />
            Future <span className="gradient-text">Leaders</span>
          </h1>
          <p className="mt-6 text-lg text-white/80 max-w-xl">
            Empowering founders and managers to leverage AI effectively. From strategy to implementation, 
            I help teams build momentum through small, compounding wins.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <a href="#contact" className="rounded-lg bg-[var(--primary-cyan)] px-5 py-3 font-medium text-black hover:opacity-90 transition-opacity">
              Book a Workshop
            </a>
            <a href="#services" className="rounded-lg border border-white/20 px-5 py-3 font-medium hover:bg-white/10 transition-colors">
              View Services
            </a>
          </div>
        </div>
        <div className="relative">
          <div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-tr from-[var(--primary-cyan)]/30 via-[var(--primary-fuchsia)]/20 to-transparent blur-2xl"/>
          <div className="relative rounded-[2rem] border border-white/10 bg-white/5 p-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="rounded-xl bg-[var(--primary-cyan)]/20 p-3">
                <svg className="h-6 w-6 text-[var(--primary-cyan)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <div className="font-semibold">Signature Framework</div>
            </div>
            <h3 className="text-xl font-bold mb-4">A.I.M — Assess · Implement · Measure</h3>
            <ul className="space-y-3 text-white/80">
              <li>• Quick AI readiness assessment</li>
              <li>• Implementation roadmap & toolkit</li>
              <li>• ROI tracking framework</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
);

// Services Section
const Services = () => {
  const services = [
    {
      title: "AI for Startups",
      description: "Practical strategies and tools to integrate AI into your startup operations.",
      features: ["Strategy workshop", "Implementation roadmap", "ROI tracking"]
    },
    {
      title: "Leadership Training",
      description: "Equip your managers to lead AI-first teams with confidence.",
      features: ["Decision frameworks", "Team enablement", "Change management"]
    },
    {
      title: "Student Programs",
      description: "Structured learning paths for students entering the AI field.",
      features: ["Hands-on projects", "Career guidance", "Industry exposure"]
    }
  ];

  return (
    <section id="services" className="bg-black/20">
      <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold">Services & Programs</h2>
          <p className="mt-4 text-lg text-white/60">Tailored solutions for different stages of your AI journey</p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div key={index} className="card-hover rounded-xl border border-white/10 bg-white/5 p-6">
              <h3 className="text-xl font-semibold mb-3">{service.title}</h3>
              <p className="text-white/60 mb-4">{service.description}</p>
              <ul className="space-y-2 text-sm text-white/80">
                {service.features.map((feature, i) => (
                  <li key={i}>• {feature}</li>
                ))}
              </ul>
              <a href="#contact" className="inline-flex items-center gap-2 mt-6 text-[var(--primary-cyan)] hover:underline">
                Learn more
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                </svg>
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Testimonials Section
const Testimonials = () => {
  const testimonials = [
    {
      quote: "Mayur's mentorship transformed how our team approaches AI. Clear frameworks, practical steps, immediate results.",
      author: "Sarah K.",
      role: "CTO, Tech Startup"
    },
    {
      quote: "The AI readiness workshop was eye-opening. We shipped our first AI feature within weeks.",
      author: "Raj P.",
      role: "Product Manager"
    },
    {
      quote: "Best investment in my AI career journey. Practical knowledge that universities don't teach.",
      author: "Emily C.",
      role: "AI Student"
    }
  ];

  return (
    <section id="testimonials" className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
      <h2 className="text-3xl font-bold text-center mb-16">What People Say</h2>
      <div className="grid md:grid-cols-3 gap-8">
        {testimonials.map((testimonial, index) => (
          <figure key={index} className="card-hover rounded-xl border border-white/10 bg-white/5 p-6">
            <blockquote className="text-lg text-white/80 mb-6">"{testimonial.quote}"</blockquote>
            <figcaption>
              <div className="font-semibold">{testimonial.author}</div>
              <div className="text-sm text-white/60">{testimonial.role}</div>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
};

// Contact Section
const Contact = () => {
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    message: ""
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you'd handle form submission here
    console.log("Form submitted:", formData);
    alert("Thanks for your message! I'll get back to you soon.");
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <section id="contact" className="relative">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(40rem_20rem_at_50%_-10%,rgba(6,249,249,0.15),transparent)]"/>
      <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold">Get in Touch</h2>
            <p className="mt-4 text-lg text-white/60">
              Let's discuss how AI can transform your business or advance your career.
            </p>
            <div className="mt-8 space-y-6">
              <div className="flex items-center gap-4">
                <div className="rounded-lg bg-white/10 p-3">
                  <svg className="h-6 w-6 text-[var(--primary-cyan)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div>
                  <div className="text-sm text-white/60">Email</div>
                  <div>mayur.prabhune@email.com</div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-lg bg-white/10 p-3">
                  <svg className="h-6 w-6 text-[var(--primary-cyan)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                </div>
                <div>
                  <div className="text-sm text-white/60">Phone</div>
                  <div>+91 87999 78054</div>
                </div>
              </div>
            </div>
          </div>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 focus:border-[var(--primary-cyan)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-cyan)]"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 focus:border-[var(--primary-cyan)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-cyan)]"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Message</label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
                rows={4}
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 focus:border-[var(--primary-cyan)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-cyan)]"
              />
            </div>
            <button
              type="submit"
              className="w-full rounded-lg bg-[var(--primary-cyan)] px-5 py-3 font-medium text-black hover:opacity-90 transition-opacity"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

// Footer Component
const Footer = () => (
  <footer className="border-t border-white/10">
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="text-white/60">
          © {new Date().getFullYear()} Mayur Prabhune. All rights reserved.
        </div>
        <div className="flex gap-8">
          <a href="#" className="text-white/60 hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" className="text-white/60 hover:text-white transition-colors">Terms of Service</a>
        </div>
      </div>
    </div>
  </footer>
);

// Main App
const App = () => (
  <React.Fragment>
    <Header />
    <main>
      <Hero />
      <Services />
      <Testimonials />
      <Contact />
    </main>
    <Footer />
  </React.Fragment>
);

// Render the app
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
