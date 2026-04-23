<?php if ( ! defined( 'ABSPATH' ) ) exit; ?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="profile" href="https://gmpg.org/xfn/11">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div class="sfx-topbar">
  <div class="wrap">
    <div class="sfx-topbar-inner">
      <span class="sfx-topbar-item"><strong>Forestry:</strong>&nbsp;<a href="tel:8437613999">(843)&nbsp;761-3999</a></span>
      <span class="sfx-topbar-div"></span>
      <span class="sfx-topbar-item"><strong>Personal:</strong>&nbsp;<a href="tel:8436280280">(843)&nbsp;628-0280</a></span>
      <span class="sfx-topbar-div"></span>
      <span class="sfx-topbar-item">Mon–Fri 8am–5pm</span>
      <span class="sfx-topbar-div"></span>
      <span class="sfx-topbar-item"><a href="mailto:info@swampfoxagency.com">info@swampfoxagency.com</a></span>
      <span class="sfx-topbar-div sfx-topbar-spacer"></span>
      <span class="sfx-topbar-item"><a href="https://portal.csr24.com/mvc/7613999" target="_blank" rel="noopener">Client&nbsp;Portal</a></span>
      <span class="sfx-topbar-div"></span>
      <span class="sfx-topbar-item"><a href="/faq/">FAQ</a></span>
      <span class="sfx-topbar-div"></span>
      <span class="sfx-topbar-item"><a href="https://www.linkedin.com/company/swamp-fox-agency/jobs/" target="_blank" rel="noopener">Careers</a></span>
    </div>
  </div>
</div>

<nav class="sfx-nav">
  <div class="wrap">
    <div class="sfx-nav-inner">
      <a class="sfx-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php bloginfo( 'name' ); ?> — Home">
        <?php if ( has_custom_logo() ) {
            the_custom_logo();
        } else { ?>
          <img src="<?php echo esc_url( get_template_directory_uri() . '/assets/logo.webp' ); ?>" alt="<?php bloginfo( 'name' ); ?>">
        <?php } ?>
      </a>
      <?php if ( has_nav_menu( 'primary' ) ) {
          wp_nav_menu( [
              'theme_location' => 'primary',
              'container'      => 'div',
              'container_class'=> 'sfx-nav-links',
              'menu_class'     => 'sfx-nav-links',
              'fallback_cb'    => 'swampfox_fallback_menu',
              'depth'          => 2,
              'items_wrap'     => '%3$s',
          ] );
      } else {
          swampfox_fallback_menu();
      } ?>
    </div>
  </div>
</nav>

<main class="sfx-content">
