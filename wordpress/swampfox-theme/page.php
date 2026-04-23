<?php if ( ! defined( 'ABSPATH' ) ) exit; get_header(); ?>

<div class="wrap" style="padding:32px clamp(20px,3vw,48px)">
  <?php while ( have_posts() ) : the_post(); ?>
    <article <?php post_class(); ?>>
      <header style="margin-bottom:22px">
        <h1><?php the_title(); ?></h1>
      </header>
      <div class="sfx-page-content">
        <?php the_content(); ?>
      </div>
    </article>
  <?php endwhile; ?>
</div>

<?php get_footer(); ?>
