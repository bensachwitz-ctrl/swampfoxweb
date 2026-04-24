// Swamp Fox Agency — shared data-layer config.
// The public site (contact / quote / newsletter forms) and this dashboard
// both read/write through this single config so everything lives in one
// "lake". Update the fields below once and both halves stay in sync.

window.SWAMPFOX_CONFIG = {
  // === Data lake (pick one and fill it in) ===========================
  // Microsoft Fabric / OneLake. If you use this, set `provider` to
  // 'onelake' and fill in the workspace + lakehouse identifiers.
  dataLake: {
    provider: 'onelake',           // 'onelake' | 'supabase' | 'airtable' | 'sheets'
    // OneLake / Fabric:
    workspace: '',                 // e.g. "swampfox-prod"
    lakehouse: '',                 // e.g. "leads_and_policies"
    tenantId: '',                  // Entra ID tenant
    // Supabase: url + anonKey
    // Airtable: baseId + tableName + token
    // Sheets:   sheetId + apiKey (via Apps Script web app)
  },

  // === Lead capture (from public site forms) =========================
  // On each public-site form submission, send a structured record here
  // in addition to emailing Benjamin@swampfoxagency.com.
  leadIngestEndpoint: '',          // e.g. 'https://api.swampfoxagency.com/leads'

  // === Dashboard access gate =========================================
  // Very light client-side gate. Replace with real auth before going
  // live — see dashboard/README.md.
  DASHBOARD_PASSWORD: '',          // empty = open (dev mode)

  // === Telematics (per-driver / per-truck) ==========================
  telematics: {
    provider: '',                  // 'samsara' | 'geotab' | 'motive' | ...
    apiBase: '',
    apiKey: '',                    // DO NOT commit a real key — pull from env at build time
  },

  // === Shared branding ==============================================
  brand: {
    name: 'Swamp Fox Insurance Agency',
    primary: '#1E392A',
    teal: '#00635B',
    gold: '#C49A3C',
    logoNav: '../images/logo-swamp-fox-nav.webp',
    logoFull: '../images/logo-swamp-fox-full.webp',
  },
};
