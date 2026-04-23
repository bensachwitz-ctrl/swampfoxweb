<?php if ( ! defined( 'ABSPATH' ) ) exit; ?>
</main>

<footer class="sfx-footer">
  <div class="wrap">
    <div class="sfx-footer-row">
      <div style="display:flex;align-items:center;gap:10px">
        <?php if ( has_custom_logo() ) { the_custom_logo(); } ?>
        <div style="font-family:'Playfair Display',serif;font-weight:700;color:#fff;font-size:.92rem;line-height:1.2">
          <?php bloginfo( 'name' ); ?>
          <span style="display:block;font-size:.65rem;font-weight:400;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:.08em;margin-top:2px;font-family:'Inter',sans-serif">Moncks Corner Roots &bull; Since 1987 &bull; SCTPA-Endorsed</span>
        </div>
      </div>
      <div style="display:flex;gap:20px;flex-wrap:wrap">
        <a href="/about/">About</a>
        <a href="/coverage/">Coverage</a>
        <a href="/summit/">Summit</a>
        <a href="/locations/">Locations</a>
        <a href="/blog/">Blog</a>
        <a href="/faq/">FAQ</a>
        <a href="https://portal.csr24.com/mvc/7613999" target="_blank" rel="noopener">Client Portal</a>
      </div>
      <div style="text-align:right">
        <a href="tel:8437613999" style="color:var(--teal-lt);font-weight:600;font-size:.82rem;display:block">(843) 761-3999</a>
        <a href="mailto:info@swampfoxagency.com" style="font-size:.72rem;color:rgba(255,255,255,.4)">info@swampfoxagency.com</a>
      </div>
    </div>
  </div>
  <div class="sfx-footer-bottom">
    <div class="wrap">
      &copy; <?php echo date( 'Y' ); ?> <?php bloginfo( 'name' ); ?>. All rights reserved. |
      <a href="/privacy/">Privacy Policy</a> | <a href="/faq/">FAQ</a> | 1122 Pinopolis Road, Moncks Corner, SC 29461
    </div>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
