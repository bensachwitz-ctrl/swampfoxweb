<?php
/**
 * Swamp Fox theme — minimal functions.
 *
 * Enqueues the theme stylesheet and Google Fonts, registers a primary
 * nav menu, and adds standard theme supports so Gutenberg renders cleanly.
 */

if ( ! defined( 'ABSPATH' ) ) exit;

function swampfox_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', [ 'search-form', 'comment-form', 'gallery', 'caption', 'style', 'script' ] );
    add_theme_support( 'responsive-embeds' );
    register_nav_menus( [
        'primary' => __( 'Primary Navigation', 'swampfox' ),
        'footer'  => __( 'Footer Navigation',  'swampfox' ),
    ] );
}
add_action( 'after_setup_theme', 'swampfox_setup' );

function swampfox_enqueue() {
    wp_enqueue_style(
        'swampfox-fonts',
        'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap',
        [], null
    );
    wp_enqueue_style(
        'swampfox-style',
        get_stylesheet_uri(),
        [ 'swampfox-fonts' ],
        wp_get_theme()->get( 'Version' )
    );
}
add_action( 'wp_enqueue_scripts', 'swampfox_enqueue' );

/**
 * Default primary-menu fallback when no menu is assigned.
 */
function swampfox_fallback_menu() {
    $items = [
        '/'                       => 'Home',
        '/coverage/'              => 'Coverage',
        '/loss-control/'          => 'Loss Control',
        '/summit/'                => 'Summit',
        '/blog/'                  => 'Blog',
        '/about/'                 => 'About',
        '/locations/'             => 'Locations',
    ];
    $current = trailingslashit( $_SERVER['REQUEST_URI'] ?? '/' );
    echo '<div class="sfx-nav-links">';
    foreach ( $items as $url => $label ) {
        $class = ( $url === $current ) ? ' current' : '';
        printf( '<a class="sfx-nav-link%s" href="%s">%s</a>', esc_attr( $class ), esc_url( $url ), esc_html( $label ) );
    }
    echo '<a class="sfx-cta" href="/contact/">Get a Quote</a>';
    echo '</div>';
}
