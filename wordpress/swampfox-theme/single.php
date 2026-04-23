<?php if ( ! defined( 'ABSPATH' ) ) exit; get_header(); ?>

<div class="wrap" style="padding:32px clamp(20px,3vw,48px)">
  <?php while ( have_posts() ) : the_post(); ?>
    <article <?php post_class(); ?> style="max-width:760px;margin:0 auto">
      <header style="margin-bottom:24px">
        <?php $cats = get_the_category(); if ( $cats ) : ?>
          <span class="label" style="color:#0F1F17;background:var(--gold-lt);border-color:rgba(196,154,60,.4)"><?php echo esc_html( $cats[0]->name ); ?></span>
        <?php endif; ?>
        <h1 style="margin:12px 0 10px"><?php the_title(); ?></h1>
        <div style="font-size:.85rem;color:var(--mid)">
          <?php echo get_the_date(); ?> &nbsp;·&nbsp; Swamp Fox Insurance Agency
        </div>
      </header>
      <div class="article-body">
        <?php the_content(); ?>
      </div>
      <aside style="margin-top:40px;padding:28px;background:linear-gradient(135deg,var(--forest),var(--teal));color:#fff;border-radius:var(--r-lg)">
        <h3 style="color:#fff;margin:0 0 10px">Talk to Swamp Fox.</h3>
        <p style="color:rgba(255,255,255,.92);margin:0 0 14px">Free policy review — no cost, no commitment. Call us or request a quote online.</p>
        <a class="btn" style="background:var(--gold-lt);color:#1A1308" href="tel:8437613999">Call (843) 761-3999</a>
        &nbsp;
        <a class="btn btn-outline" style="background:transparent;border-color:rgba(255,255,255,.5);color:#fff!important" href="/contact/">Get a Free Quote</a>
      </aside>
    </article>
  <?php endwhile; ?>
</div>

<?php get_footer(); ?>
